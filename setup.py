from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

def set_permissions_and_run_scripts():
    # Выдача прав на исполнение всем файлам в директории script/ и поддиректориях
    for root, dirs, files in os.walk('script/'):
        for file in files:
            path = os.path.join(root, file)
            os.chmod(path, 0o755)  # Установка прав на исполнение

    # Запуск скриптов config_crontab.sh и setup.broker.sh
    subprocess.call('./scripts/config_crontab.sh', shell=True)
    subprocess.call('./scripts/setup_broker.sh', shell=True)

class ScriptsSettings(install):
    def run(self):
        set_permissions_and_run_scripts()
        install.run(self)

# Определение параметров установки
setup(
    name='satellite-emulator',
    version='1.0',
    description='Project emulates threads of data in read-time',
    license='MIT',
    author='Demid Antipin, Oliferenko Maxim, Shornikov Daniil',
    url='https://github.com/PUTENCHIK/satellite-emulator',
    packages=find_packages(),
    install_requires=[
        'requests',
        'gnss-tec==1.1.1',
        'fastapi[all]',
        'uvicorn',
        'paho-mqtt',
        'schedule'
    ],
    tests_require=['pytest'],
    python_requires='>=3',
    cmdclass={
        'install': ScriptsSettings,
    }
)
