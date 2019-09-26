#include <cs50.h>
#include <stdio.h>
#include <crypt.h>
#include <stdlib.h>
#include <string.h>

void insert(const char *word);
void traverse();

struct node *start = NULL;
char *arrOfSalt[3] = {"q1", "w2", "e3"};

// Represents a node in a liked list
typedef struct node
{
    char value[3];
    struct node *next;
}
node;

int main(void)
{
    for (int i = 0; i < 3; i++)
    {
        insert(arrOfSalt[i]);
    }

    traverse();
}

// inserts a salt into a linked list
void insert(const char *word)
{
    struct node* newptr;

    // try to initiate node to insert a word
    newptr = (struct node*)malloc(sizeof(struct node)); //malloc(sizeof(node));?
    if (start == NULL)
    {
        start = newptr;
        strcpy(start->value, word);
        start -> next = NULL;
        return;
    }

    strcpy(newptr->value, word);
    newptr -> next = start;
    start = newptr;

    // // make a new pointer
    // strcpy(newptr->value, word);
    // newptr->next = NULL;
}

void traverse() {
   struct node *newptr;

   newptr = start;

   if (newptr == NULL) {
      printf("Linked list is empty.\n");
      return;
   }

   //printf("There are %d elements in linked list.\n", count);

   while (newptr->next != NULL) {
      printf("%s\n", newptr->value);
      newptr = newptr->next;
   }
   printf("%s\n", newptr->value);
}