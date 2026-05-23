package com.utilityclient.client.module.misc;

import com.utilityclient.client.UtilityClientClient;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.module.Module;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.DoubleSetting;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;

public final class ZoomModule extends Module {
    private final DoubleSetting zoomFov = addSetting(new DoubleSetting("zoomFOV", "Target zoom FOV", 25.0D, 5.0D, 70.0D));
    private final DoubleSetting smoothZoom = addSetting(new DoubleSetting("smoothZoom", "Zoom smoothing speed", 0.18D, 0.01D, 1.0D));
    private final BooleanSetting scrollToZoom = addSetting(new BooleanSetting("scrollToZoom", "Allow scroll zoom while held", true));

    private int savedFov = -1;
    private double lerpedFov = -1;

    public ZoomModule(KeyMapping keybind) {
        super("Zoom", "Hold-to-zoom utility module.", Category.MISC, keybind);
    }

    @Override
    public void onEnable() {
    }

    @Override
    public void onDisable() {
        restoreFov(Minecraft.getInstance());
    }

    @Override
    public void onTick(Minecraft client) {
        if (client.player == null) return;
        boolean held = UtilityClientClient.ZOOM_KEY.isDown();

        if (held) {
            if (savedFov < 0) {
                savedFov = client.options.fov().get();
                lerpedFov = savedFov;
            }
            double target = zoomFov.get();
            lerpedFov += (target - lerpedFov) * smoothZoom.get();
            client.options.fov().set(clamp((int) Math.round(lerpedFov)));
        } else if (savedFov >= 0) {
            lerpedFov += (savedFov - lerpedFov) * smoothZoom.get();
            if (Math.abs(lerpedFov - savedFov) < 0.5) {
                restoreFov(client);
            } else {
                client.options.fov().set(clamp((int) Math.round(lerpedFov)));
            }
        }
    }

    private void restoreFov(Minecraft client) {
        if (savedFov >= 0) {
            client.options.fov().set(savedFov);
        }
        savedFov = -1;
        lerpedFov = -1;
    }

    private static int clamp(int fov) {
        return Math.max(30, Math.min(110, fov));
    }
}
