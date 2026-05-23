package com.utilityclient.client.module.hud;

import com.utilityclient.client.mixin.FoodDataAccessor;
import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.util.RenderUtil;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.world.food.FoodData;

public final class HungerSaturationHudModule extends HudModule {
    private final BooleanSetting showSaturation = addSetting(new BooleanSetting("showSaturation", "Show hidden saturation", true));
    private final BooleanSetting showExhaustion = addSetting(new BooleanSetting("showExhaustion", "Show exhaustion", true));

    public HungerSaturationHudModule(KeyMapping keybind) {
        super("Hunger & Saturation HUD", "Food, saturation, and exhaustion HUD.", Category.HUD, keybind, 12, 12);
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
        if (!isVisible() || client.player == null) {
            return;
        }
        FoodData food = client.player.getFoodData();
        height = showExhaustion.get() ? 42 : 30;
        RenderUtil.panel(graphics, getX(), getY(), width, height);
        int hunger = food.getFoodLevel();
        int color = hunger > 14 ? 0xFF10B981 : hunger > 7 ? 0xFFFBBF24 : 0xFFEF4444;
        RenderUtil.text(graphics, "Food: " + hunger + "/20", getX() + 6, getY() + 6, color);
        if (showSaturation.get()) {
            RenderUtil.text(graphics, String.format("Sat: %.2f", food.getSaturationLevel()), getX() + 6, getY() + 18, 0xFF93C5FD);
        }
        if (showExhaustion.get()) {
            RenderUtil.text(graphics, String.format("Exh: %.2f / 4.00", ((FoodDataAccessor) food).utilityclient$getExhaustionLevel()), getX() + 6, getY() + 30, 0xFFFFFFFF);
        }
    }
}
