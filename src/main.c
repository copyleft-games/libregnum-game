/*
 * main.c - Game Entry Point
 *
 * Replace this with your actual game code.
 * See deps/libregnum/examples/ for full examples.
 *
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

#include <libregnum.h>

int
main(
    int     argc,
    char   *argv[]
){
    g_autoptr(LrgPlatformerTemplate) game = NULL;

    /*
     * Create a basic platformer using the engine template.
     * Replace LrgPlatformerTemplate with whichever template suits
     * your game, or subclass one for custom behavior.
     *
     * Available templates:
     *   LRG_TYPE_PLATFORMER_TEMPLATE
     *   LRG_TYPE_TOP_DOWN_TEMPLATE
     *   LRG_TYPE_FPS_TEMPLATE
     *   LRG_TYPE_THIRD_PERSON_TEMPLATE
     *   LRG_TYPE_TYCOON_TEMPLATE
     *   LRG_TYPE_IDLE_TEMPLATE
     *   LRG_TYPE_DECKBUILDER_COMBAT_TEMPLATE
     *   ... and more (see deps/libregnum/CLAUDE.md)
     */
    game = g_object_new(LRG_TYPE_PLATFORMER_TEMPLATE,
                         "title", GAME_NAME,
                         "virtual-width", 320,
                         "virtual-height", 240,
                         "gravity", 980.0f,
                         "jump-height", 64.0f,
                         NULL);

    return lrg_game_template_run(LRG_GAME_TEMPLATE(game), argc, argv);
}
