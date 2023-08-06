#ifndef PYBLOOMER_PLATFORM_H
#define PYBLOOMER_PLATFORM_H 1

//-----------------------------------------------------------------------------
// Platform-specific functions and macros

// Microsoft Visual Studio

#if defined(_MSC_VER)

#define FORCE_INLINE	__forceinline

// Other compilers

#else	// defined(_MSC_VER)

#ifdef __GNUC__

#define FORCE_INLINE __attribute__((always_inline)) inline

#else

#define FORCE_INLINE inline

#endif
#endif //_MSC_VER


#endif //PYBLOOMER_PLATFORM_H