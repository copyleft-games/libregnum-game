# Makefile - Libregnum Game Template
# A template for building games with libregnum
#
# Usage:
#   make                  - Build libregnum and the game
#   make game             - Build only the game (libregnum must be built)
#   make deps             - Build libregnum and its dependencies
#   make test             - Build and run the test suite
#   make run              - Build and run the game
#   make install          - Install to PREFIX
#   make clean            - Clean game build artifacts
#   make clean-all        - Clean everything (including libregnum)
#   make DEBUG=1          - Build with debug symbols
#   make ASAN=1           - Build with AddressSanitizer
#   make STATIC=1         - Build with static linking (for shipping)
#   make STEAM=1          - Build with Steam SDK support
#   make MCP=1            - Build with MCP support (AI debugging)
#   make WINDOWS=1        - Cross-compile for Windows

.DEFAULT_GOAL := all
.PHONY: all game deps test run check-deps install-deps help

# Include configuration
include config.mk

# Check dependencies before anything else (skip for bootstrap targets)
SKIP_DEP_CHECK_GOALS := install-deps help show-config check-deps clean clean-all
ifeq ($(filter $(SKIP_DEP_CHECK_GOALS),$(MAKECMDGOALS)),)
$(foreach dep,$(DEPS_REQUIRED),$(call check_dep,$(dep)))
endif

# =============================================================================
# Source Files
# =============================================================================

# Game sources (add your .c files here)
GAME_SRCS := \
	src/main.c

# Header files
GAME_HDRS := $(wildcard src/*.h src/**/*.h)

# Test sources
TEST_SRCS := $(wildcard tests/test-*.c)

# Object files
GAME_OBJS := $(patsubst src/%.c,$(OBJDIR)/%.o,$(GAME_SRCS))
TEST_OBJS := $(patsubst tests/%.c,$(OBJDIR)/tests/%.o,$(TEST_SRCS))
TEST_BINS := $(patsubst tests/%.c,$(OUTDIR)/%,$(TEST_SRCS))

# Include build rules
include rules.mk

# =============================================================================
# Targets
# =============================================================================

# Default: build deps then game
all: deps game

# Build libregnum and its dependencies
deps:
	$(call print_status,"Building libregnum...")
	@$(MAKE) -C $(LIBREGNUM_DIR) \
		DEBUG=$(DEBUG) \
		ASAN=$(ASAN) \
		UBSAN=$(UBSAN) \
		STEAM=$(STEAM) \
		MCP=$(MCP) \
		$(if $(CROSS),CROSS=$(CROSS)) \
		$(if $(filter 1,$(WINDOWS)),WINDOWS=1)

# Build the game executable
game: $(OUTDIR)/$(GAME_NAME)$(EXE_EXT)

# Build and run the game
run: all
	$(call print_status,"Running $(GAME_NAME)...")
	@LD_LIBRARY_PATH=$(LRG_LIBDIR):$(GRAYLIB_LIBDIR):$(YAMLGLIB_LIBDIR) \
		$(OUTDIR)/$(GAME_NAME)$(EXE_EXT)

# Build and run tests
test: game $(TEST_BINS)
	@echo "Running tests..."
	@failed=0; \
	for test in $(TEST_BINS); do \
		echo "  Running $$(basename $$test)..."; \
		if LD_LIBRARY_PATH=$(LRG_LIBDIR):$(GRAYLIB_LIBDIR):$(YAMLGLIB_LIBDIR) $$test; then \
			echo "    PASS"; \
		else \
			echo "    FAIL"; \
			failed=$$((failed + 1)); \
		fi \
	done; \
	if [ $$failed -gt 0 ]; then \
		echo "$$failed test(s) failed"; \
		exit 1; \
	else \
		echo "All tests passed"; \
	fi

# =============================================================================
# Dependency Checking
# =============================================================================

check-deps:
	@echo "Checking dependencies..."
	@for dep in $(DEPS_REQUIRED); do \
		if $(PKG_CONFIG) --exists $$dep; then \
			ver=$$($(PKG_CONFIG) --modversion $$dep 2>/dev/null); \
			echo "  $$dep: OK ($$ver)"; \
		else \
			echo "  $$dep: MISSING"; \
		fi \
	done
	@echo ""
	@echo "Optional dependencies:"
	@for dep in libdex-1 libsoup-3.0; do \
		if $(PKG_CONFIG) --exists $$dep; then \
			ver=$$($(PKG_CONFIG) --modversion $$dep 2>/dev/null); \
			echo "  $$dep: OK ($$ver)"; \
		else \
			echo "  $$dep: MISSING"; \
		fi \
	done
	@echo ""
	@echo "Submodule status:"
	@if [ -f "$(LIBREGNUM_DIR)/Makefile" ]; then \
		echo "  libregnum: OK"; \
	else \
		echo "  libregnum: MISSING (run: git submodule update --init --recursive)"; \
	fi

# Install build dependencies (Fedora/dnf)
install-deps:
	@echo "Installing build dependencies (Fedora)..."
	sudo dnf install -y $(FEDORA_DEPS)

# =============================================================================
# Clean (extended to handle deps)
# =============================================================================

# Override clean-all to also clean libregnum
clean-all: clean
	$(call print_status,"Cleaning libregnum...")
	@$(MAKE) -C $(LIBREGNUM_DIR) clean

# =============================================================================
# Help
# =============================================================================

help:
	@echo "$(GAME_NAME) - A libregnum game"
	@echo ""
	@echo "Build targets:"
	@echo "  all          - Build libregnum and the game (default)"
	@echo "  game         - Build only the game (libregnum must be built)"
	@echo "  deps         - Build libregnum and its dependencies"
	@echo "  test         - Build and run the test suite"
	@echo "  run          - Build and run the game"
	@echo "  install      - Install to PREFIX ($(PREFIX))"
	@echo "  uninstall    - Remove installed files"
	@echo "  clean        - Remove game build artifacts"
	@echo "  clean-all    - Remove all builds (including libregnum)"
	@echo ""
	@echo "Build options (set on command line):"
	@echo "  DEBUG=1       - Enable debug build (-g3 -O0)"
	@echo "  ASAN=1        - Enable AddressSanitizer (requires DEBUG=1)"
	@echo "  UBSAN=1       - Enable UndefinedBehaviorSanitizer (requires DEBUG=1)"
	@echo "  STATIC=1      - Static linking (for shipping)"
	@echo "  STEAM=1       - Enable Steam SDK support"
	@echo "  MCP=1         - Enable MCP support (AI debugging)"
	@echo "  WINDOWS=1     - Cross-compile for Windows (requires mingw64)"
	@echo "  GAME_NAME=x   - Set game binary name (default: $(GAME_NAME))"
	@echo "  PREFIX=path   - Set installation prefix (default: $(PREFIX))"
	@echo ""
	@echo "Utility targets:"
	@echo "  check-deps   - Check for required dependencies"
	@echo "  install-deps - Install build dependencies (Fedora/dnf)"
	@echo "  show-config  - Show current build configuration"
	@echo "  help         - Show this help message"
