"""
Django settings for momoApp project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9yn)q^btffx3-5m6%j=*lvu(nyunf+&$deyb-b1_o1za^5kw84'

DJANGO_ENV = os.getenv('DJANGO_ENV')
print('DJANGO_ENV: ' + str(DJANGO_ENV))
if str(DJANGO_ENV).__eq__('LOCALHOST'):
    DEBUG = True  # 本地开发环境下开启debug模式
    ALLOWED_HOSTS = ['*']
    DATABASES = {  # 本地开发环境数据库配置
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'momo_localhost',
            'USER': 'root',
            'PASSWORD': 'root',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
elif str(DJANGO_ENV).__eq__('DEV'):
    DEBUG = True  # 服务器开发环境下开启debug模式
    ALLOWED_HOSTS = ['*']
    DATABASES = {  # 服务器开发环境数据库配置
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'momo_dev',
            'USER': 'root',
            'PASSWORD': 'Root2019!',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
elif str(DJANGO_ENV).__eq__('PRU'):
    DEBUG = False  # 生产环境下关闭debug模式
    ALLOWED_HOSTS = ['mm.pru.igirlimg.com']
    DATABASES = {  # 生产环境数据库配置
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'momo_pru',
            'USER': 'root',
            'PASSWORD': 'Momo_pru_2019!',
            'HOST': 'localhost',
            'PORT': '3306'
        }
    }

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'user.apps.MomoappConfig'
]

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'common.util.custom_exception_handler'
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'momoApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'momoApp.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# LOGGING_DIR 日志文件存放目录
LOGGING_DIR = os.path.join(BASE_DIR, 'serverlog')
if not os.path.exists(LOGGING_DIR):
    os.mkdir(LOGGING_DIR)
LOGGING = {
    'version': 1,  # 保留字
    'disable_existing_loggers': False,  # 禁用已经存在的logger实例
    # 日志文件的格式
    'formatters': {
        # 详细的日志格式
        'standard': {
            'format': '[%(asctime)s][%(threadName)s:%(thread)d][task_id:%(name)s][%(filename)s:%(lineno)d]'
                      '[%(levelname)s][%(message)s]'
        },
        # 简单的日志格式
        'simple': {
            'format': '[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d]' + ' ==> ' + '%(message)s'
        },
        # 定义一个特殊的日志格式
        'collect': {
            'format': '%(message)s'
        }
    },
    # 过滤器
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    # 处理器
    'handlers': {
        # 在终端打印
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],  # 只有在Django debug为True时才在屏幕打印日志
            'class': 'logging.StreamHandler',  #
            'formatter': 'simple'
        },
        # 默认的
        'default': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(LOGGING_DIR, "info.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 3,  # 最多备份几个
            'formatter': 'simple',
            'encoding': 'utf-8',
        },
        # 专门用来记错误日志
        'error': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(LOGGING_DIR, "err.log"),  # 日志文件
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'standard',
            'encoding': 'utf-8',
        },
        # 专门定义一个收集特定信息的日志
        'collect': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',  # 保存到文件，自动切
            'filename': os.path.join(LOGGING_DIR, "collect.log"),
            'maxBytes': 1024 * 1024 * 50,  # 日志大小 50M
            'backupCount': 5,
            'formatter': 'collect',
            'encoding': "utf-8"
        }
    },
    'loggers': {
        # 默认的logger应用如下配置
        '': {
            'handlers': ['default', 'console', 'error'],  # 上线之后可以把'console'移除
            'level': 'DEBUG',
            'propagate': True,  # 向不向更高级别的logger传递
        },
        # 名为 'collect'的logger还单独处理
        'collect': {
            'handlers': ['console', 'collect'],
            'level': 'INFO',
        }
    },
}
