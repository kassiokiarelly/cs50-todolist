#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    string text = get_string("Text: ");

    int countLetters = 0;
    int countWords = 0;
    int countSentences = 0;

    //final sentence char code: 63,33,46,
    //space char code 32

    for (int i = 0; text[i] != '\0'; i++)
    {
        int charCode = (int)toupper(text[i]);
        if (charCode >= 65 && charCode <= 90)
        {
            countLetters++;
        }
        else if (charCode == 32)
        {
            countWords++;
        }
        else if (charCode == 33 || charCode == 46 || charCode == 63)
        {
            countSentences++;

            if (text[i + 1] == '\0') //sum last word
            {
                countWords++;
            }
        }
    }

    //printf("Letter: %i Words: %i Sentences: %i\n", countLetters, countWords, countSentences);
    //calculate grade
    //index = 0.0588 * L - 0.296 * S - 15.8
    float l = (countLetters * 100) / (float)countWords;
    float s = (countSentences * 100) / (float)countWords;
    float index = (0.0588 * l) - (0.296 * s) - 15.8;

    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %.0f\n", index);
    }
}