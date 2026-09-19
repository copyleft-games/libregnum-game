/* SPDX-License-Identifier: AGPL-3.0-or-later */
#ifndef GAME_STARTER_H
#define GAME_STARTER_H

#include <libregnum.h>

const gchar * const *game_starter_genres (void);
LrgGameTemplate *game_starter_new (const gchar *genre, GError **error);

#endif
