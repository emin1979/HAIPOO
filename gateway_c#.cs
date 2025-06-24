// В C# коде
string pythonScriptPath = "путь/к/_hon_gateway.py";
string jsonInput = "{\"operation\": \"add\", \"num1\": 10, \"num2\": 20}";

ProcessStartInfo start = new ProcessStartInfo();
start.FileName = "python"; // Или "python3" в зависимости от системы
start.Arguments = $"{pythonScriptPath} \"{jsonInput}\""; // Передача JSON как аргумента, или через StandardInput
start.UseShellExecute = false;
start.RedirectStandardOutput = true;
start.RedirectStandardInput = true; // Если будем передавать через stdin
start.CreateNoWindow = true; // Не показывать окно консоли Python

using (Process process = Process.Start(start))
{
    // Если передаем через StandardInput
    // process.StandardInput.WriteLine(jsonInput);
    // process.StandardInput.Close();

    string resultJson = process.StandardOutput.ReadToEnd();
    process.WaitForExit(); // Ждем завершения Python скрипта

    // Далее парсим resultJson в C# объект
    Console.WriteLine($"Результат от Python: {resultJson}");
}
