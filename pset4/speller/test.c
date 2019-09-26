#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

typedef struct node
{
    int val;
    struckt node * next;
} node_t;

node_t * head = NULL;
head = malloc(sizeof(node_t));
if (head == NULL)
{
    return 1;
}

head->val = 1;
head->next = NULL;

void print_list(node_t * head)
{
    node_t * current = head;

    while (current != NULL)
    {
        printf("%d\n", current->val);
        current = current->next;
    }
}

int main(void)
{

}