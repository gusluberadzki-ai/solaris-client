package com.utilityclient.client.module.mount;

import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.util.RenderUtil;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.animal.camel.Camel;
import net.minecraft.world.entity.animal.equine.AbstractHorse;
import net.minecraft.world.item.ItemStack;

public final class MountHudModule extends HudModule {
    private final BooleanSetting showMountHealth = addSetting(new BooleanSetting("showMountHealth", "Show mount health", true));
    private final BooleanSetting showMountArmor = addSetting(new BooleanSetting("showMountArmor", "Show mount armor", true));
    private final BooleanSetting showJumpMeter = addSetting(new BooleanSetting("showJumpMeter", "Show horse jump charge", true));
    private final BooleanSetting showSpearCharge = addSetting(new BooleanSetting("showSpearCharge", "Show mounted spear charge", true));

    public MountHudModule(KeyMapping keybind) {
        super("Mount HUD", "Dedicated mount HUD for horses, camels, and 1.21.11 nautilus mounts.", Category.MOUNT, keybind, 410, 12);
        width = 220;
        height = 74;
        setEnabledSilently(true);
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
        if (!isVisible() || client.player == null || !(client.player.getVehicle() instanceof LivingEntity mount)) {
            return;
        }

        RenderUtil.panel(graphics, getX(), getY(), width, height);
        int y = getY() + 6;
        RenderUtil.text(graphics, "Mount: " + mountLabel(mount), getX() + 6, y, 0xFFFFFFFF);
        y += 12;

        if (showMountHealth.get()) {
            RenderUtil.text(graphics, String.format("Health: %.1f / %.1f", mount.getHealth(), mount.getMaxHealth()), getX() + 6, y, 0xFF10B981);
            y += 12;
        }

        if (showMountArmor.get()) {
            ItemStack armor = mount.getItemBySlot(EquipmentSlot.BODY);
            String armorText = armor.isEmpty() ? "None" : armor.getHoverName().getString();
            if (!armor.isEmpty() && armor.isDamageableItem()) {
                armorText += " " + (armor.getMaxDamage() - armor.getDamageValue()) + "/" + armor.getMaxDamage();
            }
            RenderUtil.text(graphics, "Armor: " + armorText, getX() + 6, y, 0xFF93C5FD);
            y += 12;
        }

        if (showJumpMeter.get() && mount instanceof AbstractHorse) {
            RenderUtil.text(graphics, "Jump: " + String.format("%.0f%%", client.player.getJumpRidingScale() * 100.0F), getX() + 6, y, 0xFFFBBF24);
            y += 12;
        }

        if (showSpearCharge.get()) {
            ItemStack mainHand = client.player.getMainHandItem();
            if (!mainHand.isEmpty() && mainHand.getHoverName().getString().toLowerCase().contains("spear")) {
                int used = client.player.isUsingItem() ? mainHand.getUseDuration(client.player) - client.player.getUseItemRemainingTicks() : 0;
                RenderUtil.text(graphics, "Spear Charge: " + used + "t", getX() + 6, y, 0xFF8B5CF6);
            }
        }
    }

    private String mountLabel(LivingEntity mount) {
        String name = mount.getType().toString().toLowerCase();
        if (name.contains("zombie_nautilus")) return "Zombie Nautilus";
        if (name.contains("nautilus")) return "Nautilus";
        if (name.contains("camel_husk")) return "Camel Husk";
        if (name.contains("camel")) return "Camel";
        if (name.contains("zombie_horse")) return "Zombie Horse";
        if (mount instanceof Camel) return "Camel";
        return "Horse";
    }
}
