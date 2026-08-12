#include <iostream>
#include <cstdlib>
#include <string>
#include <conio.h>

using namespace std;

void decryptor()
{
    string filename;
    string password;

    cout << "Enter encrypted filename: ";
    cin >> filename;

    char ch;
    cout << "Enter password: ";
    while ((ch = _getch()) != 13) // 13 = Enter key
    {
        if (ch == 8) // Backspace
        {
            if (!password.empty())
            {
                password.pop_back();
                cout << "\b \b";
            }
        }
        else
        {
            password += ch;
            cout << '*';
        }
    }
    cout << endl;

    string command =
        "python decryptor.py \"" +
        filename +
        "\" \"" +
        password +
        "\"";

    system(command.c_str());

}