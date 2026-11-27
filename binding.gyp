{
    "targets": [
        {
            "target_name": "ag_images",
            "dependencies": [
                "./deps/libpng.gyp:libpng"
            ],
            "cflags": [
                "-Wall",
                "-Wno-unused-parameter",
                "-Wno-missing-field-initializers",
                "-Wextra",
                "-O3",
                "-fno-strict-aliasing",
                "-fvisibility=hidden",
                "-DFPNG_NO_STDIO"
            ],
            "include_dirs": [
                "<!(node -e \"require('nan')\")",
                "./deps/libpng",
                "./deps/zlib"
            ],
            "sources": [
                "./src/main.cpp"
            ],
            'conditions': [
                ['OS=="linux" and target_arch=="x64"', {
                    'cflags': [
                        '-msse4.1',
                        '-mpclmul'
                    ]
                }],
                ['OS=="mac" and target_arch=="x64"', {
                    # gyp ignores "cflags" on macOS: compiler flags go in xcode_settings.
                    # fpng's SSE 4.1 / PCLMUL path is compiled in on every x86 target
                    # (FPNG_NO_SSE defaults to 0), so clang needs these flags here too,
                    # or the build fails with "needs target feature pclmul".
                    # fpng_init() still checks the CPU at runtime before using it.
                    'xcode_settings': {
                        'OTHER_CFLAGS': [
                            '-msse4.1',
                            '-mpclmul'
                        ]
                    }
                }],
                ['OS!="linux" or target_arch!="x64"', {
                    'cflags': [
                        '-DFPNG_NO_SSE'
                    ]
                }]
            ]
        }
    ]
}
