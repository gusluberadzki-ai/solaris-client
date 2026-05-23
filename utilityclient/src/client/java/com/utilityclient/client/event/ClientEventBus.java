package com.utilityclient.client.event;

import com.utilityclient.client.UtilityClientClient;
import com.utilityclient.client.module.Module;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.rendering.v1.HudRenderCallback;
import net.fabricmc.fabric.api.client.rendering.v1.world.WorldRenderEvents;

public final class ClientEventBus {
    private ClientEventBus() {
    }

    public static void register() {
        ClientTickEvents.END_CLIENT_TICK.register(client -> {
            UtilityClientClient.handleGlobalKeys();
            for (Module module : UtilityClientClient.moduleManager.getModules()) {
                while (module.getKeybind().consumeClick()) {
                    module.toggle();
                }
                if (module.isEnabled()) {
                    module.onTick(client);
                }
            }
        });

        HudRenderCallback.EVENT.register((graphics, tickDelta) -> {
            for (Module module : UtilityClientClient.moduleManager.getModules()) {
                if (module.isEnabled()) {
                    module.onHudRender(graphics, tickDelta.getGameTimeDeltaPartialTick(false));
                }
            }
        });

        WorldRenderEvents.END_MAIN.register(context -> {
            for (Module module : UtilityClientClient.moduleManager.getModules()) {
                if (module.isEnabled()) {
                    module.onWorldRender(context);
                }
            }
        });
    }
}
