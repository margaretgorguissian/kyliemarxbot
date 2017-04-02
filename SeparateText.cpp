// SeparateText.cpp
// By: Margaret Gorguissian
// Purpose: To break up a block of text so that every 6 words a comma and 
//          quotation marks are inserted.

#include <iostream>
#include <fstream>
#include <cstdlib>
#include <vector>
#include <string>
using namespace std;

//////////////////////////// Function Declarations ////////////////////////////
vector<string> read_file(string filename);
void write_file(std::vector<string>& text, string filename);

///////////////////////////////// MAIN DRIVER /////////////////////////////////
int main()
{
        string filename;

        cout << "Please type file to read in: " << endl;
        cin >> filename;
        vector<string> text = read_file(filename);
        cout << "File sucessfully read. Now saving file.";
        write_file(text, filename);
        return 0;
}

//////////////////////////// Function Definitions /////////////////////////////
vector<string> read_file(string filename)
{
        ifstream input;
        string word;
        std::vector<string> textvector;

        input.open(filename);

        if (!input.is_open()){
                cerr << "Unable to open " << filename << endl;
                exit(1);
        }
        while (input >> word){
                if(input.eof()){
                        break;
                }
                textvector.push_back(word);
                // input >> addNum;
        }

        return textvector;
}

void write_file(std::vector<string>& text, string filename)
{       
        cerr << "in write_file\n";
        ofstream outf;
        int size = text.size();
        string newfile = filename + "Separated";
        outf.open(newfile);
        if (outf.fail()){
                exit(1);
        }

        outf << '[' << '"';
        for (int i = 0; i < size; i++){
                outf << text.at(i) << " ";
                if (i % 6 == 0){
                        outf << '"' << ", " << '"';
                }
        }
        outf << '"' << ']';
        outf.close();
}