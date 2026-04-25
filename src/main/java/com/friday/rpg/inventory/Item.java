package com.friday.rpg.inventory;

import java.io.Serializable;

public class Item implements Serializable {
    private static final long serialVersionUID = 1L;
    
    public enum ItemType { WEAPON, ARMOR, HELMET, ACCESSORY, CONSUMABLE, MATERIAL }
    
    public enum ItemRarity {
        COMMON(1.0), UNCOMMON(1.2), RARE(1.5), EPIC(2.0), LEGENDARY(3.0);
        private final double multiplier;
        ItemRarity(double multiplier) { this.multiplier = multiplier; }
        public double getMultiplier() { return multiplier; }
    }
    
    public enum ItemEffect { NONE, HEAL, RESTORE_MANA, BUFF, DAMAGE, DEBUFF }
    
    private String id;
    private String name;
    private String description;
    private ItemType type;
    private ItemRarity rarity;
    private int levelRequirement;
    private int value;
    
    private int attackBonus;
    private int defenseBonus;
    private int magicAttackBonus;
    private int magicDefenseBonus;
    private int speedBonus;
    private int healthBonus;
    private int manaBonus;
    
    private ItemEffect effect;
    private int power;
    private String icon;
    
    public Item(String id, String name, ItemType type, ItemRarity rarity) {
        this.id = id;
        this.name = name;
        this.type = type;
        this.rarity = rarity;
        this.levelRequirement = 1;
        this.effect = ItemEffect.NONE;
        this.icon = getDefaultIcon(type);
    }
    
    private String getDefaultIcon(ItemType type) {
        switch (type) {
            case WEAPON: return "⚔";
            case ARMOR: return "⛨";
            case HELMET: return "⛑";
            case ACCESSORY: return "◈";
            case CONSUMABLE: return "⚗";
            case MATERIAL: return "◆";
            default: return "?";
        }
    }
    
    public Item withDescription(String desc) {
        this.description = desc;
        return this;
    }
    
    public Item withStats(int atk, int def, int matk, int mdef, int spd) {
        this.attackBonus = atk;
        this.defenseBonus = def;
        this.magicAttackBonus = matk;
        this.magicDefenseBonus = mdef;
        this.speedBonus = spd;
        return this;
    }
    
    public Item withValue(int value) {
        this.value = value;
        return this;
    }
    
    public String getId() { return id; }
    public String getName() { return name; }
    public String getDescription() { return description; }
    public ItemType getType() { return type; }
    public ItemRarity getRarity() { return rarity; }
    public int getValue() { return value; }
    public int getAttackBonus() { return (int)(attackBonus * rarity.getMultiplier()); }
    public int getDefenseBonus() { return (int)(defenseBonus * rarity.getMultiplier()); }
    public int getMagicAttackBonus() { return (int)(magicAttackBonus * rarity.getMultiplier()); }
    public int getMagicDefenseBonus() { return (int)(magicDefenseBonus * rarity.getMultiplier()); }
    public int getSpeedBonus() { return (int)(speedBonus * rarity.getMultiplier()); }
    public String getIcon() { return icon; }
}
