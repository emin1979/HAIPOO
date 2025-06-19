// KukaBase.cs - наш первый класс для модуля Кука в проекте ХАЙПУ

using System; // Для Console.WriteLine и базовых типов

namespace Hypoo.Kuka // Определяем наше пространство имён для Куки внутри Hypoo
{
    public class KukaBase
    {
        // Свойства (поля) нашего класса
        public string Name { get; set; }
        public string Version { get; set; }

        // Конструктор класса - вызывается при создании нового объекта KukaBase
        public KukaBase(string name, string version)
        {
            Name = name;
            Version = version;
        }

        // Метод класса - действие, которое может выполнять объект KukaBase
        public void SayHello()
        {
            Console.WriteLine($"Привет! Я {Name}, версия {Version} из модуля Кука Hypoo. На связи, Эмин Джан!");
        }
    }
}
