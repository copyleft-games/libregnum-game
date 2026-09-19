/* Game starter entry point. See docs/getting-started.org.
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */
#include "game-starter.h"

int
main(
    int     argc,
    char   *argv[]
){
    g_autoptr(LrgGameTemplate) game = NULL;
    g_autoptr(GOptionContext) context = NULL;
    g_autoptr(GError) error = NULL;
    g_autofree gchar *genre = NULL;
    gboolean list_genres = FALSE;
    gboolean version = FALSE;
    GOptionEntry entries[] = {
        { "genre", 'g', 0, G_OPTION_ARG_STRING, &genre,
          "Engine template to launch (default: platformer)", "NAME" },
        { "list-genres", 0, 0, G_OPTION_ARG_NONE, &list_genres,
          "List available starters without opening a window", NULL },
        { "version", 0, 0, G_OPTION_ARG_NONE, &version,
          "Print version and license", NULL },
        { NULL, 0, 0, 0, NULL, NULL, NULL }
    };

    context = g_option_context_new ("- start a libregnum game");
    g_option_context_set_summary (context,
        "Examples:\n  " GAME_NAME " --genre top-down\n  " GAME_NAME " --list-genres");
    g_option_context_add_main_entries (context, entries, NULL);
    if (!g_option_context_parse (context, &argc, &argv, &error))
    {
        g_printerr ("%s\n", error->message);
        return 1;
    }
    if (version)
    {
        g_print ("%s %s\nAGPL-3.0-or-later\n", GAME_NAME, GAME_VERSION);
        return 0;
    }
    if (list_genres)
    {
        const gchar * const *names;
        guint i;

        names = game_starter_genres ();
        for (i = 0; names[i] != NULL; i++)
            g_print ("%s\n", names[i]);
        return 0;
    }
    if (argc != 1)
    {
        g_printerr ("Unexpected positional arguments; use --help\n");
        return 1;
    }
    game = game_starter_new (genre != NULL ? genre : "platformer", &error);
    if (game == NULL)
    {
        g_printerr ("%s\n", error->message);
        return 1;
    }
    return lrg_game_template_run (game, argc, argv);
}
