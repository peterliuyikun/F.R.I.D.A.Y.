package com.friday.rpg.inventory;

import java.io.Serializable;
import java.util.HashMap;
import java.util.Map;

public class Equipment implements Serializable {
    private static final long serialVersionUID = 1L;
    
    public enum Slot { WEAPON, ARMOR, HELMET, ACCESSORY1, ACCESSORY2 }
    
    private Map<Slot, Item> equipped;
    
    public Equipment() {
        this.equipped = new HashMap<>();
    }
    
    public boolean equip(Item item) {
        Slot slot = getSlotForItem(item);
        if (slot == null) return false;
        equipped.put(slot, item);
        return true;
    }
    
    public Item unequip(Slot slot) {
        return equipped.remove(slot);
    }
    
    public Item getEquipped(Slot slot) { return equipped.get(slot); }
    public boolean isEquipped(Item item) { return equipped.values().contains(item); }
    public boolean isSlotEmpty(Slot slot) { return !equipped.containsKey(slot); }
    
    private Slot getSlotForItem(Item item) {
        switch (item.getType()) {
            case WEAPON: return Slot.WEAPON;
            case ARMOR: return Slot.ARMOR;
            case HELMET: return Slot.HELMET;
            case ACCESSORY:
                if (isSlotEmpty(Slot.ACCESSORY1)) return Slot.ACCESSORY1;
                return Slot.ACCESSORY2;
            default: return null;
        }
    }
    
    public int getTotalAttack() {
        int total = 0;
        for (Item item : equipped.values()) total += item.getAttackBonus();
        return total;
    }
    
    public int getTotalDefense() {
        int total = 0;
        for (Item item : equipped.values()) total += item.getDefenseBonus();
        return total;
    }
    
    public int getTotalMagicAttack() {
        int total = 0;
        for (Item item : equipped.values()) total += item.getMagicAttackBonus();
        return total;
    }
    
    public int getTotalMagicDefense() {
        int total = 0;
        for (Item item : equipped.values()) total += item.getMagicDefenseBonus();
        return total;
    }
    
    public int getTotalSpeed() {
        int total = 0;
        for (Item item : equipped.values()) total += item.getSpeedBonus();
        return total;
    }
}
