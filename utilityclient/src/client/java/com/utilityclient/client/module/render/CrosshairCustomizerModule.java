package com.utilityclient.client.module.render;

import com.utilityclient.client.module.Category;
import com.utilityclient.client.module.Module;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.ColorSetting;
import com.utilityclient.client.setting.EnumSetting;
import com.utilityclient.client.setting.IntegerSetting;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;

public final class CrosshairCustomizerModule extends Module {
    public enum Shape {
        DEFAULT,
        CROSS,
        DOT,
        CIRCLE,
        PLUS
    }

    private final EnumSetting<Shape> shape = addSetting(new EnumSetting<>("shape", "Crosshair shape", Shape.CROSS, Shape.class));
    private final IntegerSetting size = addSetting(new IntegerSetting("size", "Crosshair size", 6, 1, 24));
    private final IntegerSetting thickness = addSetting(new IntegerSetting("thickness", "Crosshair thickness", 2, 1, 8));
    private final IntegerSetting gap = addSetting(new IntegerSetting("gap", "Center gap", 3, 0, 12));
    private final BooleanSetting dynamic = addSetting(new BooleanSetting("dynamic", "Expand while moving", true));
    private final ColorSetting color = addSetting(new ColorSetting("color", "RGBA color", 255, 255, 255, 255));

    public CrosshairCustomizerModule(KeyMapping keybind) {
        super("Crosshair Customizer", "Custom client crosshair overlay.", Category.RENDER, keybind);
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
        if (client.options.hideGui) {
            return;
        }
        int[] rgba = color.get();
        int argb = (rgba[3] << 24) | (rgba[0] << 16) | (rgba[1] << 8) | rgba[2];
        int cx = client.getWindow().getGuiScaledWidth() / 2;
        int cy = client.getWindow().getGuiScaledHeight() / 2;
        int extra = dynamic.get() && client.player != null && client.player.getDeltaMovement().horizontalDistanceSqr() > 0.001 ? 2 : 0;
        int actualGap = gap.get() + extra;
        if (shape.get() == Shape.DEFAULT) {
            return;
        }
        graphics.fill(cx - thickness.get(), cy - size.get() - actualGap, cx + thickness.get(), cy - actualGap, argb);
        graphics.fill(cx - thickness.get(), cy + actualGap, cx + thickness.get(), cy + size.get() + actualGap, argb);
        graphics.fill(cx - size.get() - actualGap, cy - thickness.get(), cx - actualGap, cy + thickness.get(), argb);
        graphics.fill(cx + actualGap, cy - thickness.get(), cx + size.get() + actualGap, cy + thickness.get(), argb);
        if (shape.get() == Shape.DOT || shape.get() == Shape.CIRCLE) {
            graphics.fill(cx - 1, cy - 1, cx + 1, cy + 1, argb);
        }
    }
}
