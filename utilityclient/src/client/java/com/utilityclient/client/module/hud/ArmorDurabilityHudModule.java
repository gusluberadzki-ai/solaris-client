package com.utilityclient.client.module.hud;

import com.utilityclient.client.hud.HudModule;
import com.utilityclient.client.module.Category;
import com.utilityclient.client.setting.BooleanSetting;
import com.utilityclient.client.setting.IntegerSetting;
import com.utilityclient.client.util.RenderUtil;
import java.util.ArrayList;
import java.util.List;
import net.minecraft.client.KeyMapping;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphics;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.player.Inventory;
import net.minecraft.world.item.ItemStack;

public final class ArmorDurabilityHudModule extends HudModule {
    private final BooleanSetting showNumbers = addSetting(new BooleanSetting("showNumbers", "Show durability numbers", true));
    private final IntegerSetting warningThreshold = addSetting(new IntegerSetting("warningThreshold", "Flash threshold percent", 20, 0, 100));

    public ArmorDurabilityHudModule(KeyMapping keybind) {
        super("Armor Durability HUD", "Player, spear, and mount armor durability tracking.", Category.HUD, keybind, 210, 120);
        width = 190;
        height = 90;
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
        RenderUtil.panel(graphics, getX(), getY(), width, height);
        int y = getY() + 6;

        List<ItemStack> stacks = new ArrayList<>();
        Inventory inventory = client.player.getInventory();
        stacks.add(client.player.getItemBySlot(EquipmentSlot.HEAD));
        stacks.add(client.player.getItemBySlot(EquipmentSlot.CHEST));
        stacks.add(client.player.getItemBySlot(EquipmentSlot.LEGS));
        stacks.add(client.player.getItemBySlot(EquipmentSlot.FEET));
        stacks.add(inventory.getSelectedItem());
        stacks.add(client.player.getOffhandItem());
        if (client.player.getVehicle() instanceof net.minecraft.world.entity.LivingEntity mount) {
            ItemStack armor = mount.getItemBySlot(EquipmentSlot.BODY);
            if (!armor.isEmpty()) {
                stacks.add(armor);
            }
        }

        for (ItemStack stack : stacks.stream().limit(7).toList()) {
            if (stack.isEmpty() || !stack.isDamageableItem()) {
                continue;
            }
            int max = stack.getMaxDamage();
            int remaining = max - stack.getDamageValue();
            double percent = remaining / (double) max;
            int color = RenderUtil.durabilityColor(percent);
            String text = stack.getHoverName().getString();
            if (showNumbers.get()) {
                text += " " + remaining + "/" + max;
            }
            if (stack.getHoverName().getString().toLowerCase().contains("spear")) {
                text += client.player.isUsingItem() ? " [Charge]" : " [Jab]";
            }
            RenderUtil.text(graphics, text, getX() + 6, y, color);
            y += 12;
        }
        height = Math.max(30, y - getY() + 6);
    }
}
