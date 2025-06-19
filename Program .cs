// Program.cs - Основной файл для запуска нашего приложения Hypoo

using System; // Для Console.WriteLine и базовых операций
using Hypoo.Kuka; // Для доступа к нашему классу KukaBase

namespace Hypoo // Основное пространство имён для всего проекта Hypoo
{
    class Program
    {
        static void Main(string[] args)
        {
            // Создаем экземпляр нашего класса KukaBase
            // Давай дадим ей имя "Кука" и версию "0.1 Alpha"
            KukaBase myKuka = new KukaBase("Кука", "0.1 Alpha");

            // Вызываем метод SayHello() у нашего объекта Куки
            myKuka.SayHello();

            // Добавим ещё что-нибудь, чтобы показать, что программа завершилась
            Console.WriteLine("Программа Hypoo завершила свой первый запуск.");

            // Это для того, чтобы консольное окно не закрылось сразу (если запускать без отладки)
            // Console.ReadKey(); // Закомментируем, так как на GitHub он не нужен, а может зависнуть
        }
    }
}
