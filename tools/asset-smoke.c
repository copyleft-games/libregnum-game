/* Explicit GPU smoke check; run from the repository root after assets-verify.
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */
#include <libregnum.h>

int
main(
    void
){
    g_autoptr(GrlWindow) window = NULL;
    g_autoptr(LrgAssetManager) assets = NULL;
    g_autoptr(GrlModel) model = NULL;
    g_autoptr(GError) error = NULL;
    GrlTexture *texture;

    window = grl_window_new (320, 240, "Libregnum asset smoke check");
    if (!grl_window_is_ready (window))
    {
        g_printerr ("A working graphics context is required\n");
        return 1;
    }
    assets = lrg_asset_manager_new ();
    lrg_asset_manager_add_search_path (assets, "data/assets");
    texture = lrg_asset_manager_load_texture (assets,
        "kenney-tiny-dungeon/textures/tile_0000.png", &error);
    if (texture == NULL)
    {
        g_printerr ("Texture: %s\n", error->message);
        return 1;
    }
    model = grl_model_new_from_file (
        "data/assets/kenney-platformer-kit/models/barrel.glb", &error);
    if (model == NULL)
    {
        g_printerr ("Model: %s\n", error->message);
        return 1;
    }
    if (!grl_model_is_valid (model) || grl_model_get_mesh_count (model) < 1)
    {
        g_printerr ("Model has no usable meshes\n");
        return 1;
    }
    g_print ("Loaded PNG and GLB through the pinned engine stack\n");
    /* Cleanup runs in reverse declaration order, before window destruction. */
    return 0;
}
