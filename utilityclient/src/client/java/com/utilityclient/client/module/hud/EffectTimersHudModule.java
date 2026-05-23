package com.utilityclient.client.module.hud;

import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.EnumSetting;
import com.utilityclient.client.setting.IntegerSetting;
import com.utilityclient.client.util.RenderUtil;
import java.util.Comparator;
import java.util.List;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.world.effect.MobEffectInstance;

public final class EffectTimersHudModule extends HudModule {
    public enum SortOrder {
        TIME_REMAINING,
        NAME,
        AMPLIFIER
    }

    private final BooleanSetting showIcon = addSetting(new BooleanSetting("showIcon", "Show effect icon spacing", true));
    private final BooleanSetting showAmplifier = addSetting(new BooleanSetting("showAmplifier", "Show amplifier", true));
    private final IntegerSetting maxShown = addSetting(new IntegerSetting("maxShown", "Maximum effects shown", 6, 1, 16));
    private final EnumSetting<SortOrder> sortOrder = addSetting(new EnumSetting<>("sortOrder", "Sorting mode", SortOrder.TIME_REMAINING, SortOrder.class));

    public EffectTimersHudModule(KeyMapping keybind) {
        super("Effect Timers HUD", "Potion-effect HUD with timers.", Category.HUD, keybind, 210, 12);
        width = 180;
        height = 80;
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
        List<MobEffectInstance> effects = client.player.getActiveEffects().stream().sorted(comparator()).limit(maxShown.get()).toList();
        height = Math.max(26, 14 + effects.size() * 12);
        RenderUtil.panel(graphics, getX(), getY(), width, height);
        int y = getY() + 6;
        for (MobEffectInstance effect : effects) {
            String label = effect.getEffect().value().getDisplayName().getString();
            if (showAmplifier.get()) {
                label += " " + (effect.getAmplifier() + 1);
            }
            label += " " + format(effect.getDuration());
            RenderUtil.text(graphics, (showIcon.get() ? "* " : "") + label, getX() + 6, y, 0xFFFFFFFF);
            y += 12;
        }
    }

    private Comparator<MobEffectInstance> comparator() {
        return switch (sortOrder.get()) {
            case NAME -> Comparator.comparing(effect -> effect.getEffect().value().getDisplayName().getString());
            case AMPLIFIER -> Comparator.comparingInt(MobEffectInstance::getAmplifier).reversed();
            case TIME_REMAINING -> Comparator.comparingInt(MobEffectInstance::getDuration).reversed();
        };
    }

    private String format(int ticks) {
        int totalSeconds = ticks / 20;
        return String.format("%02d:%02d", totalSeconds / 60, totalSeconds % 60);
    }
}
