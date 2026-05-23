package com.utilityclient.client.mixin;

import com.utilityclient.client.gui.SolarisScreen;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.TitleScreen;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;

@Mixin(Minecraft.class)
public abstract class MinecraftMixin {

    @Inject(method = "setScreen", at = @At("HEAD"), cancellable = true)
    private void solaris$redirectTitle(Screen screen, CallbackInfo ci) {
        if (screen instanceof TitleScreen) {
            ((Minecraft) (Object) this).setScreen(new SolarisScreen());
            ci.cancel();
        }
    }
}
