// Implements a dictionary's functionality
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 10000;

// Hash table
node *table[N];

int wordCount = 0;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    int bucket = hash(word);

    for (node *n = table[bucket]; n != NULL; n = n->next)
    {
        if (strcasecmp(n->word, word) == 0)
        {
            return true;
        }
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned int hash = 0;
    for (int i = 0, n = strlen(word); i < n; i++)
    {
        hash = (hash << 2) ^ tolower(word[i]);
    }

    return hash % N;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    FILE *file = fopen(dictionary, "r");
    if (file != NULL)
    {
        char word[LENGTH + 1];

        while (fscanf(file, "%s", word) != EOF)
        {
            node *newNode = malloc(sizeof(node));
            if (newNode == NULL)
            {
                unload();
                return false;
            }

            strcpy(newNode->word, word);
            int bucket = hash(word);
            node *tmp = table[bucket];
            newNode->next = tmp;
            table[bucket] = newNode;

            wordCount++;
        }
        fclose(file);
        return true;
    }
    return false;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return wordCount;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = N - 1; i >= 0; i--)
    {
        node *first = table[i];
        if (first != NULL)
        {
            node *a, *b;
            a = first->next;
            while (a != NULL)
            {
                b = a->next;
                free(a);
                a = b;
            }
            free(first);
        }
    }
    return true;
}
