/* SPDX-License-Identifier: AGPL-3.0-or-later */
#include "game-starter.h"

static const gchar * const genres[] = {
    "platformer", "top-down", "shooter", "twin-stick", "shmup",
    "tycoon", "racing-2d", "fps", "third-person", "racing-3d",
    "deckbuilder-combat", "deckbuilder-poker", "idle", NULL
};

const gchar * const *
game_starter_genres(
    void
){
    return genres;
}

LrgGameTemplate *
game_starter_new(
    const gchar  *genre,
    GError      **error
){
    static GType (* const types[])(void) = {
        lrg_platformer_template_get_type, lrg_top_down_template_get_type,
        lrg_shooter_2d_template_get_type, lrg_twin_stick_template_get_type,
        lrg_shmup_template_get_type, lrg_tycoon_template_get_type,
        lrg_racing_2d_template_get_type, lrg_fps_template_get_type,
        lrg_third_person_template_get_type, lrg_racing_3d_template_get_type,
        lrg_deckbuilder_combat_template_get_type,
        lrg_deckbuilder_poker_template_get_type, lrg_idle_template_get_type
    };
    guint i;

    G_STATIC_ASSERT (G_N_ELEMENTS (types) + 1 == G_N_ELEMENTS (genres));
    for (i = 0; genres[i] != NULL; i++)
    {
        if (g_strcmp0 (genre, genres[i]) == 0)
        {
            LrgGameTemplate *game;

            game = g_object_new (types[i] (), "title", GAME_NAME, NULL);
            if (LRG_IS_GAME_2D_TEMPLATE (game))
                g_object_set (game, "virtual-width", 640,
                              "virtual-height", 360, NULL);
            return game;
        }
    }

    g_set_error (error, G_OPTION_ERROR, G_OPTION_ERROR_BAD_VALUE,
                 "Unknown genre '%s'; use --list-genres", genre != NULL ? genre : "(null)");
    return NULL;
}
