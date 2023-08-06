//
// Created by Masroor Ehsan on 2023-04-28.
//
#include <io.h>
#include <stdlib.h>
#include <stdio.h>
#include <share.h>
#include <stdint.h>
#include <windows.h>

#include "io_win.h"

//ssize_t pread(int fildes, void *buf, size_t nbyte, off_t offset)
ssize_t pread(int fildes, void *buf, size_t nbyte, off_t offset) {
    if (_lseek(fildes, offset, SEEK_SET) != 0)
        return 0;

    return _read(fildes, buf, nbyte);
}


int fsync(int fd) {
    return _commit(fd);
}