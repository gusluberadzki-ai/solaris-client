package com.utilityclient.client.module.hud;

import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.util.RenderUtil;
import com.utilityclient.client.util.TpsTracker;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;

public final class FpsPerformanceHudModule extends HudModule {
    private final BooleanSetting showTps = addSetting(new BooleanSetting("showTPS", "Show estimated TPS", true));
    private final BooleanSetting showPing = addSetting(new BooleanSetting("showPing", "Show multiplayer ping", true));

    public FpsPerformanceHudModule(KeyMapping keybind) {
        super("FPS & Performance HUD", "FPS, frametime, TPS, and ping.", Category.HUD, keybind, 12, 300);
        width = 170;
        height = 54;
    }

    @Override
    public void onEnable() {
    }

    @Override
    public void onDisable() {
    }

    @Override
    public void onHudRender(GuiGraphics graphics, float tickDelta) {
        Minecraft client = Minecraft.getInstance();
        if (!isVisible()) {
            return;
        }
        int fps = Minecraft.getInstance().getFps();
        double frameMs = fps > 0 ? 1000.0D / fps : 0.0D;
        RenderUtil.panel(graphics, getX(), getY(), width, height);
        RenderUtil.text(graphics, "FPS: " + fps + " | " + String.format("%.2f ms", frameMs), getX() + 6, getY() + 6, 0xFFFFFFFF);
        int y = getY() + 18;
        if (showTps.get()) {
            double tps = TpsTracker.getTps();
            int tpsColor = tps >= 19.5 ? 0xFF10B981 : tps >= 15.0 ? 0xFFFBBF24 : 0xFFEF4444;
            RenderUtil.text(graphics, String.format("TPS est: %.1f", tps), getX() + 6, y, tpsColor);
            y += 12;
        }
        if (showPing.get() && client.getConnection() != null && client.player != null) {
            int ping = client.getConnection().getPlayerInfo(client.player.getUUID()) != null
                ? client.getConnection().getPlayerInfo(client.player.getUUID()).getLatency()
                : 0;
            RenderUtil.text(graphics, "Ping: " + ping + " ms", getX() + 6, y, 0xFF93C5FD);
        }
    }
}
