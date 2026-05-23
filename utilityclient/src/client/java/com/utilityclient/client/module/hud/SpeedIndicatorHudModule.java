package com.utilityclient.client.module.hud;

import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.util.MovementMode;
import com.utilityclient.client.util.MovementUtil;
import com.utilityclient.client.util.RenderUtil;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.world.entity.Entity;

public final class SpeedIndicatorHudModule extends HudModule {
    private final BooleanSetting showVertical = addSetting(new BooleanSetting("showVertical", "Show vertical speed", true));
    private final BooleanSetting showMaxSpeed = addSetting(new BooleanSetting("showMaxSpeed", "Track session max", true));
    private final BooleanSetting useGauge = addSetting(new BooleanSetting("useGauge", "Show a speed bar", true));
    private double sessionMax;

    public SpeedIndicatorHudModule(KeyMapping keybind) {
        super("Speed Indicator HUD", "Movement-speed HUD with 1.21.11 mount awareness.", Category.HUD, keybind, 12, 220);
        width = 168;
        height = 52;
    }

    @Override
    public void onEnable() {
        sessionMax = 0.0D;
    }

    @Override
    public void onDisable() {
    }

    @Override
    public void onHudRender(GuiGraphics graphics, float tickDelta) {
        Minecraft client = Minecraft.getInstance();
        if (!isVisible() || client.player == null) {
            return;
        }
        Entity source = client.player.getVehicle() != null ? client.player.getVehicle() : client.player;
        double horizontal = MovementUtil.horizontalSpeed(source);
        double vertical = MovementUtil.verticalSpeed(source);
        sessionMax = Math.max(sessionMax, horizontal);
        MovementMode mode = MovementUtil.mode(client.player);

        height = useGauge.get() ? 64 : 52;
        RenderUtil.panel(graphics, getX(), getY(), width, height);
        RenderUtil.text(graphics, mode.name() + ": " + String.format("%.2f b/s", horizontal), getX() + 6, getY() + 6, mode.getColor());
        if (showVertical.get()) {
            RenderUtil.text(graphics, "Vertical: " + String.format("%.2f b/s", vertical), getX() + 6, getY() + 18, 0xFFFFFFFF);
        }
        if (showMaxSpeed.get()) {
            RenderUtil.text(graphics, "Max: " + String.format("%.2f b/s", sessionMax), getX() + 6, getY() + 30, 0xFFFBBF24);
        }
        if (useGauge.get()) {
            int barWidth = (int) Math.min(width - 12, horizontal * 4.0D);
            graphics.fill(getX() + 6, getY() + height - 14, getX() + width - 6, getY() + height - 6, 0x55223344);
            graphics.fill(getX() + 6, getY() + height - 14, getX() + 6 + barWidth, getY() + height - 6, mode.getColor());
        }
    }
}
