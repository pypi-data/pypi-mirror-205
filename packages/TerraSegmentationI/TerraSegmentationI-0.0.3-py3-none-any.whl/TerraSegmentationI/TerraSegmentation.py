# Основа для модели нейронной сети
from tensorflow.keras.models import Model 

# Стандартные слои keras
from tensorflow.keras.layers import Input, Conv2DTranspose, concatenate, Activation, MaxPooling2D, Conv2D, BatchNormalization

# Оптимизатор Adam
from tensorflow.keras.optimizers import Adam 

# Дополнительные утилиты keras
from tensorflow.keras import utils 

# Инструменты для построения графиков
import matplotlib.pyplot as plt 

# Инструменты для работы с изображениями
from tensorflow.keras.preprocessing import image 

from keras.callbacks import  ReduceLROnPlateau
# Разделение данных на выборки
from sklearn.model_selection import train_test_split 

# Инструменты для работы с массивами
import numpy as np 

#для создания таблиц
import pandas as pd

from tensorflow.keras import backend as K

# Системные инструменты
import time, random, gdown, os

# Дополнительные инструменты для работы с изображениями
from PIL import Image

# работа с регулярными выражениями
import re

# Дополнительные инструменты визуализации
import seaborn as sns
sns.set_style('darkgrid')

# игнорировать предупреждения
import warnings
warnings.filterwarnings('ignore')

def dice_coef(y_true, y_pred):
    return (2. * K.sum(y_true * y_pred) + 1.) / (K.sum(y_true) + K.sum(y_pred) + 1.) # Возвращаем площадь пересечения деленную на площадь объединения двух областей



	
def load_images(folder, subset1, subset2, IMG_WIDTH, IMG_HEIGHT):
  ''' Функция загрузки изображений.
  
  folder, subset1, subset2 - каталог и подкаталоги с файлами оригинальных 
  
  и сегментированных изображений
  
  IMG_WIDTH, IMG_HEIGHT - ширина и высота изображений для загрузки 
  
  Возвращает список оригинальных изображений (image_list) 
  
  и список сегментированных изображений (mask_list) '''
  
  image_list = []
  mask_list = []
  image_format_list = []
  mask_format_list = []
  
  # расширения файлов добавляем в спсок
  for filename in sorted(os.listdir(f'{folder}/{subset1}')):
    image_format_list.append(os.path.splitext(filename)[1] )

  # загружаем изображения и добавляем имена файлов в список
    img = image.load_img(os.path.join(f'{folder}/{subset1}', filename),target_size= (IMG_HEIGHT,IMG_WIDTH))
    image_list.append(img)

  # если присутствуют разные расширения файлов, выводим предупреждение
  if len(set(image_format_list)) > 1:
    print(f'NB!В каталоге {subset1} есть файлы с разными расширениями!')
  
  print(f'Выборка {subset1} загружена, количество изображений: {len(image_list)}')
 
  # то же самое с сегментированными изображениями
  for filename in sorted(os.listdir(f'{folder}/{subset2}')):
    mask_format_list.append(os.path.splitext(filename)[1] )
    mask = image.load_img(os.path.join(f'{folder}/{subset2}', filename),target_size= (IMG_HEIGHT,IMG_WIDTH))
    mask_list.append(mask)
  
  if len(set(mask_format_list)) > 1:
    
    print(f'NB!В каталоге {subset2} есть файлы с разными расширениями!')
  
  print(f'Выборка {subset2} загружена, количество изображений: {len(mask_list)}')
 
  
  return image_list, mask_list 


def initial_analys(mask_list):

  ''' Первичный анализ изображений на предмет наличия "битых" пикселей

  mask_list - список сегментированных изображений.

  Возвращает True если есть проблема с пикселями

  и False если все в порядке

  '''

  # получаем уникальные значения цветов RGB для каждого сегментированного изображения
  for i in range(len(mask_list)):
     a = set(list(mask_list[i].getdata()))

     # если уникальных значений пикселей слишком много    
     if len(a) > 100:                  
      
      # значит скорее всего есть проблема      
       pixel_problem = True            
       print('Вероятно, в базе есть картинки с "битыми" пикселями. Это будет исправлено автоматически')
       print()
       break
       
       
     else:
       pixel_problem = False
  return pixel_problem

def pixel_get_info(mask_list, pixel_problem,IMG_HEIGHT, IMG_WIDTH):
  ''' Получение информации об уникальных значениях цветов 
  
  и частоте их встречаемости в базе. 
  
  mask_list - список сегментированных изображений

  pixel_problem - есть или нет "битые" пиксели

  IMG_HEIGHT, IMG_WIDTH - высота и ширина изображения
  
  Возвращает список уникальных значений цветов, 

  (фактически список классов) и список частот встречаемости уникальных значений.

  '''
  pixel_values_list = []

  # если есть битые пиксели
  if pixel_problem: 

    # для 100 случайных картинок приравниваем к одной из 3 категорий по условию больше/меньше
    for i in range(100):
      idx = np.random.randint(0, len(mask_list))
      y = np.array(mask_list[idx])
      y1 = np.full((IMG_HEIGHT, IMG_WIDTH,3), 100)
      y1[y < 50] = 0
      y1[y > 150] = 255
      c = list(tuple(y1[x,y,:3]) for x in range(IMG_HEIGHT) for y in range(IMG_WIDTH)) 

      #добавляем в список  значений пикселей
      pixel_values_list.extend(c)

  #если нет признаков битых пикселей    
  else:  

    #для 100 случайных картинок                                              
    for i in range(100):                               
      idx = np.random.randint(0, len(mask_list))

      #получаем значения пикселей для каждого изображения
      pixel_values = list(mask_list[idx].getdata())

      #добавляем их в список
      pixel_values_list.extend(pixel_values)

  #получаем множество уникальных значений и заодно превращаем с тип "список"
  color_list = list(set(pixel_values_list))

  #список частот уникальных значений цветов
  pix_freq = [pixel_values_list.count(i) for i in color_list] 
  count_pxl = sum(pix_freq)
  print()
  print('Проанализировано 100 случайных изображений из базы. Результат анализа:')
  print()
  print(f'Количество возможных классов {len(color_list)}.')

  # выводим результат анализа - количество возможных классов и их процентное соотношение
  for p,c,i in sorted(zip(pix_freq, color_list , range(len(color_list)))):
      print(f'{str(c).ljust(15)} - {round(p/count_pxl * 100,4)}%')

  color_list = [c for p,c in sorted(zip(pix_freq, color_list), reverse = True)]
  pix_freq = [p for p,c in sorted(zip(pix_freq, color_list), reverse = True)]

  return color_list, pix_freq 

def clip_class_number(pix_freq, color_list,pixel_problem, num_classes = None):
    ''' Изменение количества классов.

    pix_freq - список частот каждого класса

    color_list - список значений цветов

    pixel_problem - есть или нет проблема с "битыми" пикселями

    num_classes - количество классов, если известно

    Возвращает новый список цветов и список "лишних" цветов.

    '''
    #если указано количнство классов и оно совпадает с количнством автоматически определенных цветов
    if num_classes and len(color_list) == num_classes:

      # новый список цветов равен автоматически определенному
      new_color_list = color_list

      #список лишних цветов пустой
      extra_color_list = []

    # дальше два варианта  
    else:                 
        #если есть проблема с пикселям
        if pixel_problem: 

          #пытаемся найти "порог" для рекомендации по количеству классов
          for i in range(len(pix_freq) -1):  
            if pix_freq[i]/pix_freq[i+1] > 9:
              print()
              print(f'Рекомендуемое количество классов {i +1}')
              break
          # предлагаем решить сколько оставить 
          num = int(input('Сколько классов нужно оставить для обучения модели? Подтвердите рекомендуемое или измените:'))
          
        #если нет проблемы с пикселями, но при этом количество классов неизвестно или не совпало с известным
        else:                  
          # предлагаем решить сколько оставить 
          num = int(input('Сколько классов нужно оставить для обучения модели? : '))                                                 
        
        new_color_list = color_list[:num] # новый список цветов
        extra_color_list = color_list[num:]#список 'лишних' цветов
                
    
    
    return new_color_list, extra_color_list


def nearest_colour( new_color_list, extra_color ): 
    ''' Функция для определения ближайшего похожего цвета 

    из основных цветов для лишних цветов.

    new_color_list - список основных цветов

    extra_color - значение из списка "лишних" цветов

    Возвращает значение ближайшего цвета

    '''
    return min( new_color_list, key = lambda new_color_list: sum( (n - e) ** 2 for n, e in zip( new_color_list, extra_color ) ) )



def rgb_to_label(mask_list, new_color_list, extra_color_list, pixel_problem,IMG_HEIGHT, IMG_WIDTH): 
  '''Функция замены RGB на метки (индексы цветов в основном списке (new_color_list).

  Возвращает массив y_data, где значения цветов заменены на метки классов.

  mask_list - список сегментированных изображений

  new_color_list, extra_color_list - списки основных и "лишних" цветоа

  pixel_problem - есть или нет "битые" пиксели

  IMG_HEIGHT, IMG_WIDTH - высота и ширина изображения

    '''
  y_data = []

  # список индексов ближайших цветов в основном перечне цветов  для каждого "лишнего" цвета
  idx_list = [new_color_list.index((nearest_colour(new_color_list, extra_color_list[i]))) for i in range(len(extra_color_list))]

  #если есть проблема с пикселями
  if pixel_problem: 
    new_mask_list = []

    # в каждом изображении приравниваем значение пикселей к одной из трех категорий по условию больше/меньше
    for i in range(len(mask_list)):
      m = np.array(mask_list[i])                     
      m1 = np.full((IMG_HEIGHT,IMG_WIDTH, 3), 100)
      m1[m < 50] = 0
      m1[m > 150] = 255
      new_mask_list.append(m1)

      #и это будет новый список сегментированных изображений
      mask_list_1 = new_mask_list 

  #если нет проблемы с пикселями, работаем с исходным списком сегментированных изображений                      
  else:
      mask_list_1 = mask_list  

  # Для всех картинок в списке:
  for d in mask_list_1:
      sample = np.array(d)

      
      # Создание пустой 1-канальной картики
      y = np.zeros((IMG_HEIGHT,IMG_WIDTH, 1), dtype='uint8')
          
      # По всем классам:
      for i in range (len(new_color_list)):

          # если значение из списка основных цветов - присваиваем индекс этого цвета в списке  цветов(классов)
          y[np.where(np.all(sample == new_color_list[i], axis = -1))] = i 
      

      for j in range(len(extra_color_list)):

          #если значение из списка лишних цветов, присваиваем индекс ближайшего цвета
          y[np.where(np.all(sample == extra_color_list[j], axis = -1))] = idx_list[j] 
      
      y_data.append(y)
  
  return np.array(y_data)
       
           
def create_Unet(
  type_unet='m',
  img_seg_dataset = None, 
  class_list = None
):
  filters_dict = {
    's' : 16,
    'm' : 16,
    'l' : 32,
    'xl' : 32
  }

  kernel_dict = {
    's' : (2,2),
    'm' : (3,3),
    'l' : (3,3),
    'xl' : (3,4)
  }

  pool_size_dict = {
    's' : 2,
    'm' : 2,
    'l' : 2,
    'xl' : 2
  }

  num_layers_dict = {
    's' : 2,
    'm' : 3,
    'l' : 4,
    'xl' : 4
  }

  class_count = img_seg_dataset.Y["train"]["output_1"].shape[-1]
  input_shape = img_seg_dataset.X["train"]["input_1"].shape[1:]
  model_name = f'Unet-{type_unet}'

  parameters = {
    'filters': filters_dict[type_unet], 
    'kernel': kernel_dict[type_unet],
    'pool_size': pool_size_dict[type_unet],
    'num_layers': num_layers_dict[type_unet],
    'class_count': class_count,
    'input_shape':input_shape,
    'model_name': model_name 
    }

  config = get_model_Unet(
    img_seg_dataset.X["train"]["input_1"], 
    img_seg_dataset.Y["train"]["output_1"],
    class_list, 
    parameters)     
  
  return config


def train_model(
  model=None,
  img_seg_dataset='',
  batch_size=64,
  epochs=10,
  class_list=[]
):
  result = train_eval_modelUnet(
    *model, 
    img_seg_dataset.X["train"]["input_1"], 
    img_seg_dataset.Y["train"]["output_1"],
    batch_size,
    epochs, 
    class_list)
  return result

def get_data(data_list, mask_list, new_color_list, extra_color_list, pixel_problem, IMG_HEIGHT, IMG_WIDTH):
  '''Функция получения выборок для обучения '''
  x_data = []

  # оригинальные картинки просто превращаем в массивы и в общий массив
  for img in data_list:
    x = np.array(img)                
    x_data.append(x)
  x_data = np.array(x_data)

  #в сегментированных сначала меняем значения на метки и тоже преаращаем в массив
  y_data = rgb_to_label(mask_list, new_color_list, extra_color_list,pixel_problem, IMG_HEIGHT, IMG_WIDTH) 
  y_data = utils.to_categorical(y_data, len(new_color_list))

  return x_data, y_data
# Функция для просмотра изображений из набора

def show_imageset(image_list, mask_list, n):
                  
    '''Функция для просмотра изображений из набора.

    image_list, mask_list - выборки изображений

    n - количество картинок для просмотра

    '''
    # Создание полотна из n графиков в 2 ряда
    fig, axs = plt.subplots(2, n, figsize=(15, 6))      
    
    # Вывод в цикле n случайных изображений
    print('Примеры оригинальных и сегментированных изображений')
    for i in range(n): 

           # Выборка случайного фото для отображения и фото с этим же индексом из масок
          img = random.choice(image_list)       
          seg = mask_list[image_list.index(img)] 
                         
          axs[0,i].axis('off')
          axs[0,i].imshow(img)
        
          axs[1,i].axis('off')
          axs[1,i].imshow(seg)
          axs                              
    # Отрисовка изображений
    plt.show()                                           
def preprocess_data(folder, subset1, subset2, IMG_WIDTH, IMG_HEIGHT, num_classes = None):
  ''' Функция предобработки данных.

  Возвращает массивы x_data и y_data, список классов class_list
  
   '''
  cur_time = time.time()
  image_list, mask_list = load_images(folder, subset1, subset2, IMG_WIDTH, IMG_HEIGHT)
  pixel_problem = initial_analys(mask_list)
  
  
  color_list, pix_freq = pixel_get_info(mask_list, pixel_problem,IMG_HEIGHT, IMG_WIDTH)
  new_color_list, extra_color_list = clip_class_number(pix_freq, color_list,pixel_problem, num_classes)
  x_data, y_data = get_data(image_list, mask_list, new_color_list, extra_color_list, pixel_problem, IMG_HEIGHT, IMG_WIDTH)
  print()
  print(f'Сформированы выборки x_data формы {x_data.shape} и y_data формы {y_data.shape}.')
  print(f'Количество классов для обучения модели - {len(new_color_list)}.')
  print()
  print('Список классов:')
  for i, c in enumerate(new_color_list):
    print(f'{str(c).ljust(15)} - метка класса {i}')
  print()
  show_imageset(image_list, mask_list, 3)
  print()
  print(f'Обработка данных успешно завершена. Время работы - {round((time.time()- cur_time),2)} c')
  class_list = new_color_list

  return x_data, y_data, class_list  

def get_combined_colors(y_data, class_list, *mix_list):
  '''Обьединение нескольких цветов в один.

  y_data - массив сегментированных ихзображений

  class_list - список цветов(классов)

  *mix_list - списки индексов объединяемых цветов

  Возвращает новый массив y_data_mix и новый список цветов joint_color_list

  ''' 
  # список индексов цветов class_list
  class_list_idx = [i for i in range(len(class_list))] 

  # список списков индексов цветов, которые нужно обьединить
  mix_list_idx = list([*mix_list])

  # будущий список индексов цветов, которые остаются прежними, пока что это копия class_list_idx
  mono_list_idx = class_list_idx.copy() 
  
  # по длине первоначального списка классов
  for i in range(len(class_list)): 

     # если какой-то индекс есть во вложенном списке обьединяемых цветов
     if any(i in sl for sl in mix_list_idx):

        # то этот индекс удаляем из общего списка, чтобы в итоге остались только индексы одиночных цветов
        mono_list_idx.remove(class_list_idx[i])

  # делаем смешанный список индексов, его длина будет соответствовать длине нового списка цветов      
  joint_list_idx = mono_list_idx + mix_list_idx 

  # новый список цветов
  joint_color_list = []

  # по длине смешанного списка индексов
  for i in range(len(joint_list_idx)): 

     # если очередное значение из списка одиночных цветов
     if joint_list_idx[i] in mono_list_idx: 

        # то добавляем соответствующее значение этого цвета
        joint_color_list.append(class_list[joint_list_idx[i]]) 

    # если нет, то есть значение соответствует смеси цветов,    
     else:
         #добавляем нулевое значение цвета из смеси, теперь это новый цвет для всех смешиваемых категорий
         joint_color_list.append(class_list[joint_list_idx[i][0]]) 
                                                                   
  for i in range(len(joint_color_list)):
    print(f'новое значение цвета {str(joint_color_list[i]).ljust(15)} - метка (метки)  в основном перечне классов {joint_list_idx[i]}')
  
  y_data_mix = [] # новая выборка y_train
 
  
  # Для всех картинок в списке:
  for sample in y_data:
      # Создание пустой 1-канальной картики
      y = np.zeros((y_data.shape[1],y_data.shape[2], 1), dtype='uint8')
          
      # По длине списка индексов одиночных цветов:
      for i in range (len(mono_list_idx)):

        #там где значение индекса в y_train равно значению индекса одиночного цвета, меняем на новый индекс этого цвета
        y[np.where(np.all(sample == mono_list_idx[i], axis = -1))] = joint_list_idx.index(mono_list_idx[i])

      # по длине списка индексов смешанных цветов                                                                                                     
      for j in range(len(mix_list_idx)): 

        # и по длине каждого вложенного списка цветов
        for k in range(len(mix_list_idx[j])):

          # если значение равно какому либо из вложенных, меняем на новый индекс этой смеси
          y[np.where(np.all(sample == mix_list_idx[j][k], axis = -1))] = joint_list_idx.index(mix_list_idx[j]) 

      
      
      y_data_mix.append(y)
  
  return utils.to_categorical(np.array(y_data_mix), len(joint_color_list)), joint_color_list
def split_images(x_data, y_data, num_tiles):
  '''Разбиение изображений на части и формирование новых выборок x_data, y_data.

  x_data, y_data - исходные выборки

  num_tiles - необходимое количество частей каждой картинки (4, 16 ...

  '''
  
  x_data_sliced = []
  y_data_sliced = []
  M = int(x_data.shape[1] // num_tiles ** 0.5)
  N = int(x_data.shape[2] // num_tiles ** 0.5)
    
  for img in x_data:
    tiles = [img[x:x+M, y:y+N] for x in range(0, img.shape[0],M) for y in range(0, img.shape[1], N)]
    x_data_sliced.extend(tiles)

  for seg in y_data:
    segtiles = [seg[x:x+M, y:y+N] for x in range(0, seg.shape[0],M) for y in range(0, seg.shape[1], N)]
    y_data_sliced.extend(segtiles)
    
  return np.array(x_data_sliced), np.array(y_data_sliced) 
  
# Функция преобразования тензора меток класса в цветное сегметрированное изображение

def labels_to_rgb(mask_list, color_list, x_test, y_test  # список одноканальных изображений, список значений цветов
                 ):
    ''' Функция преобразования тензора меток класса в цветное сегметрированное изображение.

    mask_list - список одноканальных изображений

    color_list - список цветов

    y_test, x_test - тестовые выборки

    Возвращает массив трехканальных изображений, где на месте метки стоят значения пикселей этого цвета

    '''
    result = []

    # Для всех картинок в списке:
    for y in mask_list:
        # Создание пустой цветной картики
        temp = np.zeros(( x_test.shape[1],x_test.shape[2], 3), dtype='uint8')
        
        # По всем классам:
        for i in range(len(color_list)):

             #на том месте в пока еще пустой 3 канальной картинке, 
             #где в оригинальной картинке значение цвета равно очередному номеру класса, меняем его на значение цвета
             temp[np.where(np.all(y == i, axis = -1))] = (color_list[i]) 
            
        
        # когда по всему списку прошлись, добавляем получившееся в result
        result.append(temp)

    # и превращаем его в массив
    return np.array(result)

def enter_parameters_Unet(x_data, y_data, class_list): 
  '''Получение списка параметров модели Unet '''
  
  # предлагаем ввести нужные параметры модели
  filters = int(input('Число фильтров в начальном слое сверточного блока (filters):  '))
  kernel = input('Размер ядра свертки(kernel):  '.ljust(62)) 
  if str.isnumeric(kernel):
     kernel = tuple([int(kernel), int(kernel)])
  else:
     kernel = tuple(int(s) for s in (re.findall('\d+', kernel)))

  
  pool_size = int(input('Размер max_pooling (pool_size): '.ljust(62)))
  num_layers = int(input('Количество блоков в ветке U-net (num_layers): '.ljust(62)))
  model_name = input('Имя модели: '.ljust(62))
  class_count = len(class_list)
  
   # проверяем корректность введенного значения num_layers
  max_num_layers = 0
  a,b = x_data.shape[2],x_data.shape[1]                
  for i in range(num_layers):
      a = a/pool_size
      b = b/pool_size
      if a == int(a) and b == int(b):
          max_num_layers += 1
      
  if num_layers > max_num_layers:
    print()
    print(f'NB!Максимально допустимая величина num_layers при данном размере изображения и значении pool_size - {max_num_layers}')

    # если нужно - корректируем num_layers
    num_layers = max_num_layers                        
    print()
    print(f'Скорректированное значение num_layers - {num_layers}')
  
  input_shape = (x_data.shape[1], x_data.shape[2], 3)                     
  
  # возвращает список парвметров модели, нужный потом для вывода статистики обучения
  return filters, kernel,pool_size, num_layers,class_count, input_shape, model_name 

def conv_block_unet(x, filters, kernel): 
  
    # создаем сверточный блок U_net
    x = Conv2D(filters = filters, kernel_size = kernel,strides = 1, padding='same')(x)     
    x = BatchNormalization()(x)                                           
    x = Activation('relu')(x) 
    
    x = Conv2D(filters = filters, kernel_size = kernel,strides = 1, padding='same')(x) 
    x = BatchNormalization()(x)
    x = Activation('relu')(x) 
    block_out = x                                     
    
    return x,   block_out                                 
def transpose_block_unet(x, filters, kernel, pool_size): 
  
    # создаем "повышающий" блок U_net
    x = Conv2DTranspose(filters = filters, kernel_size = kernel,strides = pool_size, padding='same')(x)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)
                                                 
    return x

def create_unet(filters, kernel,pool_size, num_layers,class_count,input_shape, model_name): # строим U_net
  
        '''Создание модели U_net '''

        input_image = Input((input_shape))   
        x = input_image
        # пустой список для выходов после каждого сверточного блока
        out_list = [] 
        
        # пустой список для количеств фильтров фильтров в каждом сверточном блоке                         
        filters_list = []                      
      
        # первая ветка сети, количество фильтров в каждом блоке увеличивается, размерность уменьшается
        for i in range(num_layers): 

          #добавляем в список количество фильтров каждого блока
          filters_list.append(filters * 2 ** i) 
          
          x,  block_out = conv_block_unet(x, filters  = filters * 2 ** i, kernel = kernel)
          
          x = MaxPooling2D(pool_size)(block_out)

          #добавляем выходы каждого блока
          out_list.append(block_out)           

        #переворачиваем списки, чтобы использовать их дальше в обратном порядке  
        out_list = list(reversed(out_list))             
        filters_list = list(reversed(filters_list))

        # центральный блок, количество фильтров предыдущего слоя увеличиваем в два раза
        x, _ = conv_block_unet(x, filters  = x.shape[-1] * 2, kernel = kernel) 
        
        
        # вторая ветка сети, количество фильтров в каждом блоке уменьшается (берем из перевернутого списка), размерность увеличивается
        for i in range(num_layers):
          x = transpose_block_unet(x, filters = filters_list[i], kernel = kernel, pool_size = pool_size)

          # в каждом блоке - конкатенация с соответствующим выходом первой ветки (тоже берем из перевернутого списка)
          x = concatenate([x, out_list[i]])
          x, _ = conv_block_unet(x, filters  = filters_list[i], kernel = kernel)
        
        output = Conv2D(class_count, (3, 3), activation='softmax', padding='same')(x)
      
              
        model = Model(input_image, output,
                      name = model_name)
        model.compile(optimizer=Adam(learning_rate=1e-4),
                  loss='categorical_crossentropy',
                  metrics=[dice_coef])

        return model
def get_model_Unet(x_data, y_data, class_list, parameters_dict = None):
  
  '''Создание модели и фиксация ее параметров ''' 

  # если берем параметры из словаря
  if parameters_dict:
    
    # проверяем корректность значения num_layers
    max_num_layers = 0
    a,b = x_data.shape[2],x_data.shape[1]                 
    for i in range(parameters_dict['num_layers']):
       a = a/parameters_dict['pool_size']
       b = b/parameters_dict['pool_size']
       if a == int(a) and b == int(b):
          max_num_layers += 1
      
    if parameters_dict['num_layers'] > max_num_layers:
      print()
      print(f'NB!Максимально допустимая величина num_layers при данном размере изображения и значении pool_size - {max_num_layers}')

      # если нужно - корректируем num_layers
      parameters_dict['num_layers'] = max_num_layers                         
      print()
      print(f'Скорректированное значение num_layers - {max_num_layers}')
    parameters = list(parameters_dict.values())
  
  # если нет словаря параметров
  else:
    # то выполняется функция enter_parameters_Unet
    parameters = enter_parameters_Unet(x_data, y_data, class_list)
  model = create_unet(*parameters)
  return model, parameters
# Функция визуализации процесса сегментации изображений - случайные изображения

def process_images(
	model,
	color_list,
	x_test, 
	y_test,
	count = 1,
	need_best=False,				   
	):
    '''Функция визуализации процесса сегментации изображений - случайные изображения

    model - обученная модель

    color_list - список цветов

    x_test, y_test - тестовые выборки

    count - количество картинок

    '''
	
	
    if need_best:
      accuracy_list = np.array([model.evaluate(x_test[i:i+1], 
                        y_test[i:i+1],
                        verbose=0)[1] for i in range(x_test.shape[0])])	
      indexes = np.argsort(accuracy_list)[-5:].tolist()
    
    else:
      # Генерация случайного списка индексов в количестве count между (0, len(x_test)
      indexes = np.random.randint(0, len(x_test), count)
    
    # Вычисление предсказания сети для картинок с отобранными индексами
    predict = np.argmax(model.predict(x_test[indexes],verbose=0), axis=-1)

    # Подготовка цветов классов для отрисовки предсказания
    orig = labels_to_rgb(predict[..., None], color_list, x_test, y_test)
    fig, axs = plt.subplots(3, count, figsize=(15, 12)) 
    
    # Отрисовка результата работы модели
    for i in range(count):
        # Отображение на графике в первой линии предсказания модели
        axs[0, 0].set_title('Результат работы модели - случайные изображения:')
        axs[0, i].imshow(orig[i])
        axs[0, i].axis('off')

        # Отображение на графике во второй линии сегментированного изображения из y_test
        axs[1, 0].set_title('Оригинальное сегментированное')
        axs[1, i].imshow(labels_to_rgb(np.argmax(y_test[indexes], axis=-1)[..., None], color_list, x_test, y_test)[i])       
        axs[1 ,i].axis('off')

        # Отображение на графике в третьей линии оригинального изображения
        axs[2, 0].set_title('Оригинальное изображение')
        axs[2, i].imshow(x_test[indexes[i]])
        axs[2 ,i].axis('off')

    plt.show() 
# Функция визуализации результата работы модели - лучшие и худшие изображения

	
def process_images_1(model, 
                     color_list,                      
                     count,
                     x_test, y_test,                     
                     indexes_best,                
                     indexes_bad):
    '''Функция визуализации результата работы модели - лучшие и худшие изображения

    model - обученная модель

    color_list - список цветов

    x_test, y_test - тестовые выборки

    count - количество картинок

    indexes_best, indexes_bad - индексы лучших и худших картинок

    '''
                

    # Вычисление предсказания сети для картинок с отобранными индексами
    predict_best = np.argmax(model.predict(x_test[indexes_best], verbose = 0), axis=-1)
    predict_bad = np.argmax(model.predict(x_test[indexes_bad], verbose = 0), axis=-1)

    # Подготовка цветов классов для отрисовки предсказания
    orig_best = labels_to_rgb(predict_best[..., None],color_list, x_test, y_test)
    orig_bad = labels_to_rgb(predict_bad[..., None],color_list, x_test, y_test)
    
    fig, axs = plt.subplots(6, count, figsize=(12, 20)) 
    
    # Отрисовка результата работы модели
    for i in range(count):
        # Отображение на графике в первой линии предсказания модели
        axs[0, 0].set_title('Результат работы модели - лучшие изображения:')
        axs[0, i].imshow(orig_best[i])
        axs[0, i].axis('off')

        axs[1, 0].set_title('Оригинальное сегментированное')
        axs[1, i].imshow(labels_to_rgb(np.argmax(y_test[indexes_best], axis=-1)[..., None], color_list, x_test, y_test)[i])
        axs[1 ,i].axis('off')

        axs[2, 0].set_title('Оригинальное изображение')
        axs[2, i].imshow(x_test[indexes_best[i]])
        axs[2 ,i].axis('off')

        axs[3, 0].set_title('Результат работы модели -худшие изображения:')
        axs[3, i].imshow(orig_bad[i])
        axs[3, i].axis('off')

        # Отображение на графике во второй линии сегментированного изображения из y_test
        axs[4, 0].set_title('Оригинальное сегментированное')
        axs[4, i].imshow(labels_to_rgb(np.argmax(y_test[indexes_bad], axis=-1)[..., None], color_list, x_test, y_test)[i])
        axs[4 ,i].axis('off')

        # Отображение на графике в третьей линии оригинального изображения
        axs[5, 0].set_title('Оригинальное изображение')
        axs[5, i].imshow(x_test[indexes_bad[i]])
        axs[5 ,i].axis('off')

    plt.show() 
def train_eval_modelUnet(model, parameters, x_data, y_data, batch_size, epochs, class_list): # обучение и оценка модели

  '''Обучение и оценка модели

  model, parameters - модель с заданными параметрами

  x_data, y_data - выборки для обучения

  class_list - список классов(цветов)

  '''
                           

  # формируем тренировочную, валидационную и тестовую выборки
  x_train,x_val, y_train, y_val = train_test_split(x_data, y_data, test_size = 0.2, shuffle = True, random_state = 6) 
  x_train,x_test, y_train, y_test = train_test_split(x_train, y_train, test_size = 0.1, shuffle = True, random_state = 6)

  reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.6, patience=5, verbose=0) 

  # обучаем                                
  history = model.fit(x_train, y_train,
                        epochs=epochs, batch_size=batch_size,
                         validation_data=(x_val, y_val),callbacks=reduce_lr) 

  # выводим график обучения                                          
  plt.figure(figsize=(10, 5))
  plt.plot(history.history['dice_coef'])                                                              
  plt.plot(history.history['val_dice_coef'])
  plt.show()

  # оцениваем на тестовой выборке
  acc = model.evaluate(x_test,y_test, verbose=0)[1]                                                                
 
  print(f'Средняя точность модели на тестовой выборке: {acc}')

  # рисуем случайные картинки из предикта
  process_images(model, class_list,x_test, y_test,3, True)                                                                     
  
  # сохраняем параметры модели и обучения для итоговой статистики
  parameters_list = ['filters', 'kernel','pool_size','num_layers','batch_size', 'dice_coef']                              
  values_list = [(parameters[0]),(parameters[1]),(parameters[2]), (parameters[3]),(batch_size),acc]
  model_list = [model.name]

  result_table = pd.DataFrame(values_list).T
  result_table.columns = parameters_list
  result_table.index = model_list
  result_table[['filters', 'pool_size','num_layers','batch_size']] = result_table[['filters', 'pool_size','num_layers','batch_size']].astype(int)
  
  # сохраняем итоги в таблицу
  return  result_table                                                                                                   
  
      
 # вывод лучших и худших результатов модели
def best_worst_result(model,x_data, y_data, class_list):                                                                  
  x_train,x_val, y_train, y_val = train_test_split(x_data, y_data, test_size = 0.2, shuffle = True, random_state = 6)
  x_train,x_test, y_train, y_test = train_test_split(x_train, y_train, test_size = 0.1, shuffle = True, random_state = 6)
  accuracy_list = np.array([model.evaluate(x_test[i:i+1], 
                                         y_test[i:i+1],
                                         verbose=0)[1] for i in range(x_test.shape[0])])
  bad = np.argsort(accuracy_list)[:5].tolist()
  best = np.argsort(accuracy_list)[-5:].tolist()
  process_images_1(model, class_list, 3,x_test, y_test, best, bad)

  # финальная таблица результатов после обучения нескольких вариантов архитектур модели
def final_result(*result_tabels):    
  print('Итоговая таблица результатов')
  df = pd.concat([*result_tabels])
  df.fillna(0, inplace=True)
  dtype_dict = {col: int for col in df.columns if col not in ['kernel', 'dice_coef']}

  # преобразуем типы данных в DataFrame
  df = df.astype(dtype_dict)

  
  return df.style.background_gradient(subset='dice_coef')
  
def enter_parameters_PSP(x_data, y_data, class_list):

  '''Получение списка параметров модели PSPnet '''                
  
  filters = int(input('Число фильтров в каждом слое сверточного блока (filters):  '.ljust(62)))
  kernel = input('Размер ядра свертки(kernel):  '.ljust(62)) 
  if str.isnumeric(kernel):
     kernel = tuple([int(kernel), int(kernel)])
  else:
     kernel = tuple(int(s) for s in (re.findall('\d+', kernel)))
  pool_number = int(input('Количество блоков maxPooling (pool_number): '.ljust(62)))
  conv_number = int(input('Количество сверточных блоков (conv_number): '.ljust(62)))
  model_name = input('Имя модели: '.ljust(62))
  class_count = len(class_list)
  
  # проверяем корректность введенного значения pool_number
  max_pool_number = 0
  a,b = x_data.shape[2],x_data.shape[1]                                  
  for i in range(pool_number):
      c = a/2**(i+1)
      d = b/2**(i+1)
      if c == int(c) and d == int(d):
          max_pool_number += 1
      
  if pool_number > max_pool_number:                                      
    print()
    print(f'NB!Максимально допустимая величина pool_number при данном размере изображения  - {max_pool_number}')

    # если нужно - корректируем
    pool_number = max_pool_number
    print()
    print(f'Скорректированное значение pool_number - {pool_number}')
  
  input_shape = (x_data.shape[1], x_data.shape[2], 3)                     
  

  return filters, kernel,pool_number, conv_number,class_count, input_shape, model_name   

# сверточный блок PSPnet
def conv_block_PSP(x,filters, kernel):                              
  x = Conv2D(filters = filters, kernel_size = kernel, padding='same' )(x)     
  x = BatchNormalization()(x)                                           
  x = Activation('relu')(x) 
    
  x = Conv2D(filters = filters, kernel_size = kernel, padding='same')(x) 
  x = BatchNormalization()(x)
  x = Activation('relu')(x)
  block_out = x 

  return x,block_out

 # блок пулинга PSPnet
def pool_block_PSP(block_out,pool_number,filters, kernel): 

  # список для сохранения выходов блоков               
  pool_out_list = [] 

  # по количеству блоков MaxPooling
  for i in range(pool_number):  
    
    # увеличиваем в 2 раза размер пулинга                       
    pool_size = 2 ** (i+1) 

    #добавляем  MaxPooling в нужном количестве, все присоединяем к одному выходу block_out
    x = MaxPooling2D(pool_size)(block_out)  

    # к каждому добавляем сверточный слой             
    x = Conv2D(filters, kernel, padding='same', activation='relu')(x)
 
    # и слой Conv2DTranspose, в котором увеличиваем размерность обратно до исходной
    pool_out = Conv2DTranspose( filters,(pool_size, pool_size), strides=(pool_size, pool_size), activation='relu')(x) 
    
    # получившиеся выходы добавляем в список
    pool_out_list.append(pool_out) 
   
  
  # возвращает список выходов каждого блока пулинга
  return  pool_out_list                                   

def create_PSPnet(filters, kernel, pool_number,conv_number,class_count,input_shape, model_name): 
  '''Построение модели PSPnet '''
  
  img_input = Input(input_shape)
  x = img_input
  block_out_list = []
  
  # входной сверточный блок в количестве conv_number
  for i in range(conv_number):
     x, block_out = conv_block_PSP(x,filters, kernel)          
     block_out_list.append(block_out)

  # блок MaxPooling в количестве pool_number
  pool_out_list = pool_block_PSP(block_out,pool_number,filters, kernel) 
  
  # конкатенация выходов сверточных блоков и блоков пулинга
  x = concatenate(pool_out_list + block_out_list) 

  # еще сверточный блок           
  x, _ = conv_block_PSP(x,filters, kernel)                   

  output = Conv2D(class_count, (3, 3), activation='softmax', padding='same')(x)
  
          
  model = Model(img_input, output, name = model_name)
  model.compile(optimizer=Adam(learning_rate=1e-4),
                  loss='categorical_crossentropy',
                  metrics=[dice_coef])
  return model

  
  

def get_model_PSP(x_data, y_data,class_list, parameters_dict = None):
  ''' Получение модели PSPnet с заданными параметрами '''

  # если есть словарь параметров
  if parameters_dict:

    # проверяем корректность  значения pool_number
    max_pool_number = 0
    a,b = x_data.shape[2],x_data.shape[1]                                 
    for i in range(parameters_dict['pool_number']):
      c = a/2**(i+1)
      d = b/2**(i+1)
      if c == int(c) and d == int(d):
          max_pool_number += 1
      
    if parameters_dict['pool_number'] > max_pool_number:                                     
      print()
      print(f'NB!Максимально допустимая величина pool_number при данном размере изображения  - {max_pool_number}')

      # если нужно - корректируем
      parameters_dict['pool_number'] = max_pool_number
      print()
      print(f'Скорректированное значение pool_number - {max_pool_number}')
    parameters = list(parameters_dict.values())

  # если нет словаря параметров
  else:
    # выполняется функция enter_parameters_PSP
    parameters = enter_parameters_PSP(x_data, y_data, class_list)

  # создаем модель
  model = create_PSPnet(*parameters)

  return model, parameters
def train_eval_modelPSP(model, parameters, x_data, y_data, batch_size, epochs, class_list): 
  '''Обучение и оценка модели '''
                
                
  # делим данные на тренировочную, проверочную и тестовую выборки
  x_train,x_val, y_train, y_val = train_test_split(x_data, y_data, test_size = 0.2, shuffle = True, random_state = 6)  
  x_train,x_test, y_train, y_test = train_test_split(x_train, y_train, test_size = 0.1, shuffle = True, random_state = 6)

  reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.6, patience=5)

  # обучаем
  history = model.fit(x_train, y_train,                                                                                
                        epochs=epochs, batch_size=batch_size,
                         validation_data=(x_val, y_val),callbacks=reduce_lr)
  
  # выводим график обучения
  plt.figure(figsize=(10, 5))                                                                
  plt.plot(history.history['dice_coef'])
  plt.plot(history.history['val_dice_coef'])
  plt.show()                                                                                                            
 
  # оцениваем на тестовой выборке
  acc = model.evaluate(x_test,y_test, verbose=0)[1]                                                               
 
  print(f'Средняя точность модели на тестовой выборке: {acc}')

  # рисуем случайные картитнки
  process_images(model, class_list,x_test, y_test,3)                                                                   
  
  parameters_list = ['filters', 'kernel', 'pool_number','conv_number','batch_size', 'dice_coef']
  values_list = [parameters[0],parameters[1],parameters[2], parameters[3],batch_size,acc]
  model_list = [model.name]
  
  # сохраняем параметры модели и обучения в таблицу
  result_table = pd.DataFrame(values_list).T                                                                            
  result_table.columns = parameters_list
  result_table.index = model_list
  result_table[['filters', 'pool_number','conv_number','batch_size']] = result_table[['filters','pool_number','conv_number','batch_size']].astype(int)
  
  return  result_table
  
      
