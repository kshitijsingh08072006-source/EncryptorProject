#include <iostream>
#include <cstdlib>
#include "encryptor.h"
#include "decryptor.h"

using namespace std;

int main()
{
    int choice;

    while (true)
    {
        cout << "\n=====================\n";
        cout << "      ENC_DCP\n";
        cout << "=====================\n";
        cout << "1. Encrypt File\n";
        cout << "2. Decrypt File\n";
        cout << "3. Exit\n";
        cout << "\nChoice: ";

        cin >> choice;

        if (choice == 1)
        {
            encryptor();
        }
        else if (choice == 2)
        {
            decryptor();
        }
        else if (choice == 3)
        {
            cout << "Goodbye!\n";
            break;
        }
        else
        {
            cout << "Invalid choice!\n";
        }
    }

    return 0;
}