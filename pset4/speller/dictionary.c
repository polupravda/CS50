// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>

#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 2600

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

bool insert(int key, const char *word);

int wordCount = 0;

// Represents a hash table
node *hashtable[N] = {NULL};
node* newptr;
int hashedValue;

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    //return tolower(word[0]) - 'a';

    unsigned int sum = 0;
    int wordLength = strlen(word);

    // convert a word into an int, which represents a sum of all charecters and put it into a hashtable
    for (int i = 0; i < wordLength; i++)
    {
        sum += tolower(word[i]) - '0';
    }
    unsigned int hashBucket = sum % N;
    return hashBucket;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        // create root for hashtable
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // hash a word
        hashedValue = hash(word);

        // load the word into a table with hashed value
        insert(hashedValue, word);
        wordCount++;
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // check if there are words
    if (wordCount == 0)
    {
        unload();
        return 0;
    }
    return wordCount;
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
        int bucket = hash(word);
        node *cursor = hashtable[bucket];

        while (cursor != NULL)
        {
            if (strcasecmp(word, cursor->word) == 0)
            {
                return true;
            }
            cursor = cursor->next;
        }
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = hashtable[i];

        while (cursor != NULL)
        {
            node *temp = cursor;
            cursor = cursor->next;
            free(temp);
        }
    }
    return true;
}

// inserts a word into a dictionary
bool insert(int key, const char *word)
{
    // try to initiate node to insert a word
    newptr = malloc(sizeof(node));
    if (newptr == NULL)
    {
        unload();
        return false;
    }

    // make a new pointer
    strcpy(newptr->word, word);
    newptr->next = NULL;

    // check for empty list
    if (hashtable[key] == NULL)
    {
        hashtable[key] = newptr;
    }
    // check for insertion at the beginning of the linked list
    else {
        newptr->next = hashtable[key];
        hashtable[key] = newptr;
    }
    return true;
}