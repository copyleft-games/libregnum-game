# rules.mk - Libregnum Game Template Build Rules
#
# Pattern rules and common build recipes for game projects.

# =============================================================================
# Terminal Colors
# =============================================================================

ifneq ($(TERM),)
    TPUT := $(shell which tput 2>/dev/null)
    ifneq ($(TPUT),)
        COLORS := $(shell $(TPUT) colors 2>/dev/null)
    endif
endif

ifeq ($(shell test $(COLORS) -ge 8 2>/dev/null && echo yes),yes)
    COLOR_RESET := $(shell $(TPUT) sgr0)
    COLOR_BOLD := $(shell $(TPUT) bold)
    COLOR_RED := $(shell $(TPUT) setaf 1)
    COLOR_GREEN := $(shell $(TPUT) setaf 2)
    COLOR_YELLOW := $(shell $(TPUT) setaf 3)
    COLOR_BLUE := $(shell $(TPUT) setaf 4)
    COLOR_CYAN := $(shell $(TPUT) setaf 6)
else
    COLOR_RESET :=
    COLOR_BOLD :=
    COLOR_RED :=
    COLOR_GREEN :=
    COLOR_YELLOW :=
    COLOR_BLUE :=
    COLOR_CYAN :=
endif

# =============================================================================
# Output Functions
# =============================================================================

define print_status
	@printf "$(COLOR_GREEN)$(COLOR_BOLD)==>$(COLOR_RESET) %s\n" $(1)
endef

define print_warning
	@printf "$(COLOR_YELLOW)$(COLOR_BOLD)Warning:$(COLOR_RESET) %s\n" $(1)
endef

define print_error
	@printf "$(COLOR_RED)$(COLOR_BOLD)Error:$(COLOR_RESET) %s\n" $(1)
endef

define print_info
	@printf "$(COLOR_CYAN)Info:$(COLOR_RESET) %s\n" $(1)
endef

define print_compile
	@printf "  $(COLOR_BLUE)CC$(COLOR_RESET)      %s\n" $(1)
endef

define print_link
	@printf "  $(COLOR_BLUE)LINK$(COLOR_RESET)    %s\n" $(1)
endef

# =============================================================================
# Directory Creation
# =============================================================================

$(BUILDDIR):
	@$(MKDIR_P) $(BUILDDIR)

$(OBJDIR): | $(BUILDDIR)
	@$(MKDIR_P) $(OBJDIR)

$(OUTDIR): | $(BUILDDIR)
	@$(MKDIR_P) $(OUTDIR)

# =============================================================================
# Source Compilation
# =============================================================================

# Generic pattern rule: src/**/*.c -> obj/**/*.o
$(OBJDIR)/%.o: src/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(call print_compile,$<)
	@$(CC) $(GAME_CFLAGS) -MMD -MP -c $< -o $@

# =============================================================================
# Game Executable
# =============================================================================

$(OUTDIR)/$(GAME_NAME)$(EXE_EXT): $(GAME_OBJS) | $(OUTDIR)
	$(call print_link,"$(GAME_NAME)$(EXE_EXT)")
	@$(CC) -o $@ $(GAME_OBJS) $(GAME_LDFLAGS) $(GAME_LIBS)

# =============================================================================
# Test Compilation
# =============================================================================

$(OBJDIR)/tests/%.o: tests/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(call print_compile,$<)
	@$(CC) $(TEST_CFLAGS) -MMD -MP -c $< -o $@

$(OUTDIR)/test-%: $(OBJDIR)/tests/test-%.o $(filter-out $(OBJDIR)/main.o,$(GAME_OBJS)) | $(OUTDIR)
	$(call print_link,"test-$*")
	@$(CC) -o $@ $< $(filter-out $(OBJDIR)/main.o,$(GAME_OBJS)) $(TEST_LDFLAGS) $(TEST_LIBS)

# =============================================================================
# Clean Rules
# =============================================================================

.PHONY: clean clean-all
clean:
	$(call print_status,"Cleaning $(BUILD_TYPE) build...")
	rm -rf $(BUILDDIR)/$(BUILD_TYPE)

clean-all:
	$(call print_status,"Cleaning all builds...")
	rm -rf $(BUILDDIR)

# =============================================================================
# Installation Rules
# =============================================================================

.PHONY: install uninstall

install: $(OUTDIR)/$(GAME_NAME)$(EXE_EXT)
	$(call print_status,"Installing $(GAME_NAME)...")
	$(MKDIR_P) $(DESTDIR)$(BINDIR)
	$(INSTALL_PROGRAM) $(OUTDIR)/$(GAME_NAME)$(EXE_EXT) $(DESTDIR)$(BINDIR)/

uninstall:
	$(call print_status,"Uninstalling $(GAME_NAME)...")
	rm -f $(DESTDIR)$(BINDIR)/$(GAME_NAME)$(EXE_EXT)

# =============================================================================
# Dependency Tracking
# =============================================================================

-include $(GAME_OBJS:.o=.d)
-include $(TEST_OBJS:.o=.d)
