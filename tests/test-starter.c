/* SPDX-License-Identifier: AGPL-3.0-or-later */
#include "game-starter.h"

static void
test_genres(
    void
){
    const gchar * const *names;
    guint i;

    names = game_starter_genres ();
    for (i = 0; names[i] != NULL; i++)
    {
        g_autoptr(LrgGameTemplate) game = NULL;
        g_autoptr(GError) error = NULL;
        g_autofree gchar *title = NULL;

        game = game_starter_new (names[i], &error);
        g_assert_no_error (error);
        g_assert_true (LRG_IS_GAME_TEMPLATE (game));
        g_object_get (game, "title", &title, NULL);
        g_assert_cmpstr (title, ==, GAME_NAME);
        if (LRG_IS_GAME_2D_TEMPLATE (game))
        {
            gint width;
            gint height;

            g_object_get (game, "virtual-width", &width, "virtual-height", &height, NULL);
            g_assert_cmpint (width, ==, 640);
            g_assert_cmpint (height, ==, 360);
        }
    }
    g_assert_cmpuint (i, ==, 13);
}

static void
test_unknown(
    void
){
    g_autoptr(GError) error = NULL;

    g_assert_null (game_starter_new ("platfomer", &error));
    g_assert_error (error, G_OPTION_ERROR, G_OPTION_ERROR_BAD_VALUE);
    g_clear_error (&error);
    g_assert_null (game_starter_new (NULL, &error));
    g_assert_error (error, G_OPTION_ERROR, G_OPTION_ERROR_BAD_VALUE);
}

int
main(
    int    argc,
    char **argv
){
    g_test_init (&argc, &argv, NULL);
    g_test_add_func ("/starter/genres", test_genres);
    g_test_add_func ("/starter/unknown", test_unknown);
    return g_test_run ();
}
