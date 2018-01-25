# Intro to the Command line

This page is here to help lesson the learning curve for new members of ACM who have never used a 
commandline. Currently this contains only a guide for `BASH` (Bourne Again Shell), but may contain guides 
for other shells and a guide for mac users with `Homebrew`.

## Anatomy of the Terminal

start out by launching a terminal, it will look like this.

[username@localmachine ~ ] $ 

you should see your username name before the @ symbol.
 This is followed by the name of your computer and the ~ means that the terminal is currently lookin at your
home directory. This is where input commands.

### <span style="color:red">**Important note!**</span>

 If you see the name `root` here it means that you are running the terminal as a very powerful user named 
 `root`. `root` has ultimate privaliges on your machine and might as well be god as far as your computer is 
 conserned. With great power comes great responcibility and running as root is considered very dangerous 
 because you can easily destroy your operating system. To switch out of root type:

    $ su yourUserName

## Useful Commands

    $ cd directory/
This lets you change the directory that you are in. This is how you will navigate your computer

    $ ls
This will show you every file and directory in you current working directory (this is displayed where that ~ was when you first loaded up the terminal).

    $ pwd
This is short for "print working directory." This will show you where your terminal is looking at.

    $ man <command>
This brings up the manual page for whatever comand you specify. This will be your best friend!

    $ mkdir

## <span style="color:yellow">Don't Panic</span>
There is a lot ot learn when it comes to learning the comand line, and you will not be expected to learn everything all at once. You are also not alone, feel free to ask other ACM members  for help. Included below are some places where you can learn more.

- Linuxcommand.org 
    - This is a good place to start, and will teach you everything from your first command to making `BASH` scripts.
- More is to come in the future

