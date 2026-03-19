# Git Useful Commands

## Configuration

git config --global user.name "Your Name"       # set global username
git config --global user.email "you@email.com"  # set global email
git config --list                               # list all config values

## Repositoryw

git init                        # initialize new local repo
git clone <url>                 # clone remote repo locally

## Status and History

git status                      # show working tree status
git log --oneline               # compact commit history
git log --oneline --graph       # history with branch graph
git diff                        # show unstaged changes
git diff --staged               # show staged changes

## Staging and Committing

git add .                           # stage all changes
git add <file>                      # stage specific file
git commit -m "message"             # commit with message
git commit --amend -m "message"     # edit last commit message

## Branches

git branch                      # list local branches
git branch <name>               # create new branch
git checkout <name>             # switch to branch
git checkout -b <name>          # create and switch to branch
git merge <name>                # merge branch into current
git branch -d <name>            # delete merged branch
git branch -D <name>            # force delete branch

## Remote

git remote -v                           # list remotes
git remote add origin <url>             # add remote origin
git fetch --all                         # fetch all remotes without merging
git pull origin <branch>                # fetch and merge remote branch
git push origin <branch>                # push branch to remote
git push --force-with-lease             # safe force push

## Tags

git tag                                        # list all tags
git tag -a v1.0 -m "message"                   # create annotated tag at HEAD
git tag -a v1.0 <commit-hash> -m "message"     # create tag at specific commit
git tag -d v1.0                                # delete tag locally
git push origin v1.0                           # push specific tag
git push origin --delete v1.0                  # delete tag remotely
git fetch --tags                               # fetch all remote tags

## Undoing Changes

git restore <file>                  # discard unstaged changes in file
git restore --staged <file>         # unstage a file
git revert <commit-hash>            # create new commit that undoes a commit
git reset --soft HEAD~1             # undo last commit, keep changes staged
git reset --hard HEAD~1             # undo last commit, discard all changes

## Stash

git stash                       # stash current changes
git stash pop                   # apply last stash and remove it
git stash list                  # list all stashes
git stash drop                  # delete last stash
