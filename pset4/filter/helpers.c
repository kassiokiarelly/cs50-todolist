#include "helpers.h"
#include <math.h>
#include <stdlib.h>

// >>>>>>>> auxiliary functions

int min(int a, int b)
{
    if (a < b)
    {
        return a;
    }
    return b;
}

int max(int a, int b)
{
    if (a > b)
    {
        return a;
    }
    return b;
}

void set(RGBTRIPLE *pixel, int red, int green, int blue)
{
    pixel->rgbtRed = min(255, red);
    pixel->rgbtGreen = min(255, green);
    pixel->rgbtBlue = min(255, blue);
    return;
}

void swap(RGBTRIPLE *p1, RGBTRIPLE *p2)
{
    RGBTRIPLE tmp;
    tmp = *p1;
    *p1 = *p2;
    *p2 = tmp;
}

void copy(int width, int height, RGBTRIPLE from[height][width], RGBTRIPLE to[height][width])
{
    for (int x = 0; x < width; x++)
    {
        for (int y = 0; y < height; y++)
        {
            to[y][x].rgbtRed = from[y][x].rgbtRed;
            to[y][x].rgbtGreen = from[y][x].rgbtGreen;
            to[y][x].rgbtBlue = from[y][x].rgbtBlue;
        }
    }
}

// <<<<<<<<

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int x = 0; x < width; x++)
    {
        for (int y = 0; y < height; y++)
        {
            RGBTRIPLE *p = &image[y][x];
            if (p->rgbtBlue == p->rgbtGreen && p->rgbtGreen == p->rgbtRed)
            {
                continue;
            }
            else
            {
                float sum = p->rgbtRed + p->rgbtGreen + p->rgbtBlue;
                float avg = sum / 3;
                int value = round(avg);
                set(p, value, value, value);
            }
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int x = 0; x < width; x++)
    {
        for (int y = 0; y < height; y++)
        {
            RGBTRIPLE *p = &image[y][x];
            float red =   .393 * p->rgbtRed + .769 * p->rgbtGreen + .189 * p->rgbtBlue;
            float green = .349 * p->rgbtRed + .686 * p->rgbtGreen + .168 * p->rgbtBlue;
            float blue =  .272 * p->rgbtRed + .534 * p->rgbtGreen + .131 * p->rgbtBlue;
            set(p, round(red), round(green), round(blue));
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    //RGBTRIPLE *tmp = (RGBTRIPLE*)malloc(sizeof(RGBTRIPLE));


    for (int y = 0; y < height; y++)
    {
        int left = 0;
        int right = width - 1;
        while (left < right)
        {
            swap(&image[y][left], &image[y][right]);
            left++;
            right--;
        }
    }
    //free(tmp);
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE b[height][width];

    int x_min = 0;
    int x_max = 0;
    int y_min = 0;
    int y_max = 0;

    int red = 0;
    int green = 0;
    int blue = 0;

    float avgRed = 0;
    float avgGreen = 0;
    float avgBlue = 0;

    int pointsCount = 0;

    for (int x = 0; x < width; x++)
    {
        x_max = min(x + 1, width - 1);
        x_min = max(x - 1, 0);

        for (int y = 0; y < height; y++)
        {
            y_max = min(y + 1, height - 1);
            y_min = max(y - 1, 0);

            red = 0;
            green = 0;
            blue = 0;
            pointsCount = 0;

            for (int x_now = x_min; x_now <= x_max; x_now++)
            {
                for (int y_now = y_min; y_now <= y_max; y_now++)
                {
                    red += image[y_now][x_now].rgbtRed;
                    green += image[y_now][x_now].rgbtGreen;
                    blue += image[y_now][x_now].rgbtBlue;

                    pointsCount++;
                }
            }

            avgRed = red / pointsCount;
            avgGreen = green / pointsCount;
            avgBlue = blue / pointsCount;

            b[y][x].rgbtRed = round(avgRed);
            b[y][x].rgbtGreen = round(avgGreen);
            b[y][x].rgbtBlue = round(avgBlue);
        }
    }

    for (int x = 0; x < width; x++)
    {
        for (int y = 0; y < height; y++)
        {
            image[y][x].rgbtRed = b[y][x].rgbtRed;
            image[y][x].rgbtGreen = b[y][x].rgbtGreen;
            image[y][x].rgbtBlue = b[y][x].rgbtBlue;
        }
    }

    return;
}

