//
// Created by Masroor Ehsan on 2023-04-28.
//

#ifndef _SYS_IO_WIN_H
#define _SYS_IO_WIN_H 1

#include <sys/types.h>
#include "unistd.h"

ssize_t pread(int fildes, void *buf, size_t nbyte, off_t offset);
int fsync (int fd);

#endif //_SYS_IO_WIN_H
