# config.mk - Libregnum Game Template Configuration
#
# This file contains all configurable build options.
# Override any variable on the command line:
#   make DEBUG=1
#   make GAME_NAME=my-game

# =============================================================================
# Game Configuration
# =============================================================================

# Game name (used for binary name and defines)
# Override this with your actual game name
GAME_NAME ?= libregnum-game

# Game version
VERSION_MAJOR := 0
VERSION_MINOR := 1
VERSION_MICRO := 0
VERSION := $(VERSION_MAJOR).$(VERSION_MINOR).$(VERSION_MICRO)

# =============================================================================
# Build Options
# =============================================================================

# Debug build mode:
#   0 = Release build (-O2, no debug symbols)
#   1 = Debug build (-g3 -O0, full debug info for gdb)
DEBUG ?= 0

# Enable AddressSanitizer (requires DEBUG=1)
ASAN ?= 0

# Enable UndefinedBehaviorSanitizer (requires DEBUG=1)
UBSAN ?= 0

# Build unit tests
BUILD_TESTS ?= 1

# Static linking mode (for shipping)
STATIC ?= 0

# =============================================================================
# Dependency Paths
# =============================================================================

# Libregnum and its transitive dependencies
LIBREGNUM_DIR := $(CURDIR)/deps/libregnum
GRAYLIB_DIR := $(LIBREGNUM_DIR)/deps/graylib
YAMLGLIB_DIR := $(LIBREGNUM_DIR)/deps/yaml-glib

# =============================================================================
# Steam SDK Integration (Opt-In)
# =============================================================================
#
# Usage: make STEAM=1
#
# Requires: Steamworks SDK configured in libregnum

STEAM ?= 0

# =============================================================================
# MCP Support (Opt-In) - For AI-assisted debugging
# =============================================================================
#
# Usage: make MCP=1
#
# Requires: mcp-glib in libregnum/deps/mcp-glib

MCP ?= 0

# =============================================================================
# Installation Directories
# =============================================================================

PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin
DATADIR ?= $(PREFIX)/share

# =============================================================================
# Compiler and Tools
# =============================================================================

CC := gcc
AR := ar
PKG_CONFIG ?= pkg-config
INSTALL := install
INSTALL_PROGRAM := $(INSTALL) -m 755
INSTALL_DATA := $(INSTALL) -m 644
MKDIR_P := mkdir -p

# =============================================================================
# Platform Detection
# =============================================================================

UNAME_S := $(shell uname -s)
UNAME_M := $(shell uname -m)

ifeq ($(UNAME_S),Linux)
    PLATFORM := linux
else ifeq ($(UNAME_S),FreeBSD)
    PLATFORM := freebsd
else ifeq ($(UNAME_S),Darwin)
    PLATFORM := macos
else ifneq (,$(findstring MINGW,$(UNAME_S)))
    PLATFORM := windows
else
    PLATFORM := unknown
endif

# =============================================================================
# Windows Cross-Compilation Support
# =============================================================================
#
# Usage: make WINDOWS=1

WINDOWS ?= 0
CROSS ?=

ifeq ($(WINDOWS),1)
    CROSS := x86_64-w64-mingw32
endif

ifneq ($(CROSS),)
    CC := $(CROSS)-gcc
    AR := $(CROSS)-ar
    PKG_CONFIG := $(CROSS)-pkg-config
    TARGET_PLATFORM := windows
    EXE_EXT := .exe
else
    TARGET_PLATFORM := $(PLATFORM)
    EXE_EXT :=
endif

# =============================================================================
# Build Directories
# =============================================================================

BUILDDIR := build

ifeq ($(DEBUG),1)
    OBJDIR := $(BUILDDIR)/debug/obj
    OUTDIR := $(BUILDDIR)/debug
    BUILD_TYPE := debug
else
    OBJDIR := $(BUILDDIR)/release/obj
    OUTDIR := $(BUILDDIR)/release
    BUILD_TYPE := release
endif

# =============================================================================
# Libregnum Build Directories
# =============================================================================

ifeq ($(DEBUG),1)
    LRG_BUILDDIR := $(LIBREGNUM_DIR)/build/debug
else
    LRG_BUILDDIR := $(LIBREGNUM_DIR)/build/release
endif

LRG_LIBDIR := $(LRG_BUILDDIR)/lib
LRG_STATIC := $(LRG_LIBDIR)/liblibregnum.a
LRG_SHARED := $(LRG_LIBDIR)/liblibregnum.so

GRAYLIB_LIBDIR := $(GRAYLIB_DIR)/build/lib
GRAYLIB_STATIC := $(GRAYLIB_LIBDIR)/libgraylib.a

YAMLGLIB_LIBDIR := $(YAMLGLIB_DIR)/build
YAMLGLIB_STATIC := $(YAMLGLIB_LIBDIR)/libyaml-glib.a

RAYLIB_STATIC := $(GRAYLIB_DIR)/deps/raylib/src/libraylib.a

# =============================================================================
# Compiler Flags
# =============================================================================

# C standard (gnu89, NO -pedantic)
CSTD := -std=gnu89

# Warning flags
WARN_CFLAGS := -Wall -Wextra -Werror
WARN_CFLAGS += -Wformat=2 -Wformat-security
WARN_CFLAGS += -Wnull-dereference
WARN_CFLAGS += -Wstrict-prototypes
WARN_CFLAGS += -Wmissing-prototypes
WARN_CFLAGS += -Wold-style-definition
WARN_CFLAGS += -Wdeclaration-after-statement
WARN_CFLAGS += -Wno-unused-parameter

# Feature test macros
FEATURE_CFLAGS := -D_GNU_SOURCE

# Debug/Release flags
ifeq ($(DEBUG),1)
    OPT_CFLAGS := -g3 -O0 -DDEBUG
else
    OPT_CFLAGS := -O2 -DNDEBUG
endif

# Sanitizer flags
ifeq ($(ASAN),1)
ifeq ($(DEBUG),1)
    OPT_CFLAGS += -fsanitize=address -fno-omit-frame-pointer
    SANITIZER_LIBS := -fsanitize=address
endif
endif

ifeq ($(UBSAN),1)
ifeq ($(DEBUG),1)
    OPT_CFLAGS += -fsanitize=undefined
    SANITIZER_LIBS += -fsanitize=undefined
endif
endif

# =============================================================================
# Dependency pkg-config
# =============================================================================

# Core GLib dependencies (required)
GLIB_CFLAGS := $(shell $(PKG_CONFIG) --cflags glib-2.0 gobject-2.0 gio-2.0 gmodule-2.0)
GLIB_LIBS := $(shell $(PKG_CONFIG) --libs glib-2.0 gobject-2.0 gio-2.0 gmodule-2.0)

# json-glib (required by libregnum)
JSON_CFLAGS := $(shell $(PKG_CONFIG) --cflags json-glib-1.0)
JSON_LIBS := $(shell $(PKG_CONFIG) --libs json-glib-1.0)

# libdex for async (optional, not for Windows cross-compile)
ifeq ($(TARGET_PLATFORM),windows)
    DEX_CFLAGS :=
    DEX_LIBS :=
else
    DEX_CFLAGS := $(shell $(PKG_CONFIG) --cflags libdex-1 2>/dev/null)
    DEX_LIBS := $(shell $(PKG_CONFIG) --libs libdex-1 2>/dev/null)
endif

# =============================================================================
# Game Version Defines
# =============================================================================

VERSION_CFLAGS := -DGAME_VERSION=\"$(VERSION)\"
VERSION_CFLAGS += -DGAME_VERSION_MAJOR=$(VERSION_MAJOR)
VERSION_CFLAGS += -DGAME_VERSION_MINOR=$(VERSION_MINOR)
VERSION_CFLAGS += -DGAME_VERSION_MICRO=$(VERSION_MICRO)
VERSION_CFLAGS += -DGAME_NAME=\"$(GAME_NAME)\"

# =============================================================================
# Include Paths
# =============================================================================

GAME_INC := -I$(CURDIR)/src
GAME_INC += -I$(LIBREGNUM_DIR)/src
GAME_INC += -I$(GRAYLIB_DIR)/src
GAME_INC += -I$(GRAYLIB_DIR)/deps/raylib/src
GAME_INC += -I$(YAMLGLIB_DIR)/src

# =============================================================================
# Composite Flags
# =============================================================================

GAME_CFLAGS := $(CSTD) $(WARN_CFLAGS) $(FEATURE_CFLAGS) $(OPT_CFLAGS)
GAME_CFLAGS += $(VERSION_CFLAGS)
GAME_CFLAGS += $(GAME_INC)
GAME_CFLAGS += $(GLIB_CFLAGS) $(DEX_CFLAGS) $(JSON_CFLAGS)
GAME_CFLAGS += -DG_LOG_USE_STRUCTURED
GAME_CFLAGS += -DG_LOG_DOMAIN=\"$(GAME_NAME)\"

# Steam flags (passed through to libregnum)
ifeq ($(STEAM),1)
    STEAM_SDK_PATH := $(LIBREGNUM_DIR)/deps/steamworks_sdk/sdk
    GAME_CFLAGS += -I$(STEAM_SDK_PATH)/public -DLRG_ENABLE_STEAM=1
    ifeq ($(TARGET_PLATFORM),windows)
        STEAM_LIBS := -L$(STEAM_SDK_PATH)/redistributable_bin/win64 -lsteam_api64
    else
        STEAM_LIBS := -L$(STEAM_SDK_PATH)/redistributable_bin/linux64 -lsteam_api
    endif
endif

# MCP flags (passed through to libregnum)
ifeq ($(MCP),1)
    MCP_GLIB_DIR := $(LIBREGNUM_DIR)/deps/mcp-glib
    GAME_CFLAGS += -I$(MCP_GLIB_DIR)/src -DLRG_ENABLE_MCP=1
    MCP_LIBS := -L$(MCP_GLIB_DIR)/build -lmcp-glib-1.0
endif

# =============================================================================
# Linker Flags
# =============================================================================

# Platform-specific system libraries
ifeq ($(TARGET_PLATFORM),windows)
    PLATFORM_LIBS := -lopengl32 -lgdi32 -lwinmm -lshell32
else
    PLATFORM_LIBS := -lGL -lm -lpthread -ldl -lrt -lX11
endif

ifeq ($(STATIC),1)
    # Static linking: link .a files directly in dependency order
    GAME_LDFLAGS :=
    ifeq ($(TARGET_PLATFORM),windows)
        GAME_LDFLAGS += -static
    else
        GAME_LDFLAGS += -static-libgcc
    endif
    GAME_LIBS := -Wl,--allow-multiple-definition
    GAME_LIBS += $(LRG_STATIC)
    GAME_LIBS += $(GRAYLIB_STATIC)
    GAME_LIBS += $(YAMLGLIB_STATIC)
    GAME_LIBS += $(RAYLIB_STATIC)
    GAME_LIBS += $(shell $(PKG_CONFIG) --static --libs glib-2.0 gobject-2.0 gio-2.0 gmodule-2.0)
    GAME_LIBS += $(shell $(PKG_CONFIG) --static --libs json-glib-1.0)
    GAME_LIBS += $(shell $(PKG_CONFIG) --static --libs yaml-0.1)
    GAME_LIBS += $(shell $(PKG_CONFIG) --static --libs libsoup-3.0 2>/dev/null)
    ifneq ($(TARGET_PLATFORM),windows)
        GAME_LIBS += $(shell $(PKG_CONFIG) --static --libs libdex-1 2>/dev/null)
    endif
    GAME_LIBS += -lm $(PLATFORM_LIBS) $(SANITIZER_LIBS)
    GAME_LIBS += $(STEAM_LIBS) $(MCP_LIBS)
else
    # Dynamic linking
    GAME_LDFLAGS := -L$(LRG_LIBDIR)
    GAME_LDFLAGS += -L$(GRAYLIB_LIBDIR)
    GAME_LDFLAGS += -L$(YAMLGLIB_LIBDIR)
    ifeq ($(TARGET_PLATFORM),windows)
        # Windows: DLLs must be in PATH or same directory
    else
        GAME_LDFLAGS += -Wl,-rpath,'$$ORIGIN/../../$(LRG_LIBDIR)'
        GAME_LDFLAGS += -Wl,-rpath,'$$ORIGIN/../../$(GRAYLIB_LIBDIR)'
        GAME_LDFLAGS += -Wl,-rpath,'$$ORIGIN/../../$(YAMLGLIB_LIBDIR)'
    endif
    ifeq ($(MCP),1)
        GAME_LDFLAGS += -L$(MCP_GLIB_DIR)/build
        ifneq ($(TARGET_PLATFORM),windows)
            GAME_LDFLAGS += -Wl,-rpath,'$$ORIGIN/../../$(MCP_GLIB_DIR)/build'
        endif
    endif
    GAME_LIBS := -llibregnum -lgraylib -lyaml-glib -lm
    GAME_LIBS += $(GLIB_LIBS) $(DEX_LIBS) $(JSON_LIBS)
    GAME_LIBS += $(SANITIZER_LIBS)
    GAME_LIBS += $(STEAM_LIBS) $(MCP_LIBS)
    ifeq ($(TARGET_PLATFORM),windows)
        GAME_LIBS += $(PLATFORM_LIBS)
    endif
endif

# =============================================================================
# Test Flags
# =============================================================================

TEST_CFLAGS := $(GAME_CFLAGS)
ifeq ($(STATIC),1)
    TEST_LDFLAGS := $(GAME_LDFLAGS)
    TEST_LIBS := $(GAME_LIBS)
else
    TEST_LDFLAGS := $(GAME_LDFLAGS) -Wl,-rpath,$(LRG_LIBDIR)
    TEST_LIBS := $(GAME_LIBS)
endif

# =============================================================================
# Check for required dependencies
# =============================================================================

define check_dep
$(if $(shell $(PKG_CONFIG) --exists $(1) && echo yes),,$(error Missing dependency: $(1)))
endef

# Required system packages
DEPS_REQUIRED := glib-2.0 gobject-2.0 gio-2.0 gmodule-2.0
DEPS_REQUIRED += json-glib-1.0

# Fedora package names for dependencies
FEDORA_DEPS := gcc make pkgconf-pkg-config
FEDORA_DEPS += glib2-devel json-glib-devel
FEDORA_DEPS += libdex-devel libyaml-devel libsoup3-devel
FEDORA_DEPS += gobject-introspection-devel
FEDORA_DEPS += mesa-libGL-devel libX11-devel

# =============================================================================
# Print Configuration
# =============================================================================

.PHONY: show-config
show-config:
	@echo "$(GAME_NAME) Build Configuration"
	@echo "=================================="
	@echo "Version:      $(VERSION)"
	@echo "Build type:   $(BUILD_TYPE)"
	@echo "Compiler:     $(CC)"
	@echo "Platform:     $(TARGET_PLATFORM)"
	@echo "PREFIX:       $(PREFIX)"
	@echo "DEBUG:        $(DEBUG)"
	@echo "ASAN:         $(ASAN)"
	@echo "UBSAN:        $(UBSAN)"
	@echo "STATIC:       $(STATIC)"
	@echo "STEAM:        $(STEAM)"
	@echo "MCP:          $(MCP)"
	@echo "BUILD_TESTS:  $(BUILD_TESTS)"
	@echo ""
	@echo "GAME_CFLAGS:  $(GAME_CFLAGS)"
	@echo "GAME_LDFLAGS: $(GAME_LDFLAGS)"
	@echo "GAME_LIBS:    $(GAME_LIBS)"
