package com.friday.rpg.core;

import com.friday.rpg.inventory.Item;
import com.friday.rpg.inventory.ItemDatabase;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class Enemy implements Serializable {
    private static final long serialVersionUID = 1L;
    
    public enum EnemyType { DROID, BEAST, SITH, MERCENARY, CREATURE, BOSS }
    
    private String name;
    private EnemyType type;
    private int level;
    
    private int maxHealth;
    private int currentHealth;
    private int attack;
    private int defense;
    private int magicAttack;
    private int magicDefense;
    private int speed;
    
    private int xpReward;
    private int goldReward;
    private List<Item> lootTable;
    private double lootChance;
    
    public Enemy(String name, EnemyType type, int level) {
        this.name = name;
        this.type = type;
        this.level = level;
        this.lootTable = new ArrayList<>();
        generateStats();
    }
    
    private void generateStats() {
        double hpMult = 1.0, atkMult = 1.0, defMult = 1.0, spdMult = 1.0;
        
        switch (type) {
            case DROID: hpMult = 0.8; atkMult = 1.2; defMult = 1.3; spdMult = 0.7; break;
            case BEAST: hpMult = 1.3; atkMult = 1.4; defMult = 0.6; spdMult = 1.1; break;
            case SITH: hpMult = 1.0; atkMult = 1.3; defMult = 0.9; spdMult = 1.2; break;
            case MERCENARY: hpMult = 1.1; atkMult = 1.1; defMult = 1.0; spdMult = 1.0; break;
            case CREATURE: hpMult = 0.9; atkMult = 0.9; defMult = 0.8; spdMult = 1.3; break;
            case BOSS: hpMult = 3.0; atkMult = 1.5; defMult = 1.3; spdMult = 0.9; break;
        }
        
        int base = level * 10;
        this.maxHealth = (int)(base * hpMult * 5);
        this.currentHealth = maxHealth;
        this.attack = (int)(base * atkMult * 0.8);
        this.defense = (int)(base * defMult * 0.5);
        this.magicAttack = (int)(base * atkMult * 0.6);
        this.magicDefense = (int)(base * defMult * 0.4);
        this.speed = (int)(base * spdMult * 0.3);
        
        this.xpReward = level * 20 + (int)(Math.random() * level * 10);
        this.goldReward = level * 5 + (int)(Math.random() * level * 3);
        this.lootChance = 0.3;
        
        if (Math.random() < 0.5) lootTable.add(ItemDatabase.getRandomConsumable(level));
        if (Math.random() < 0.3) lootTable.add(ItemDatabase.getRandomEquipment(level));
    }
    
    public static Enemy generateRandom(int playerLevel) {
        EnemyType[] types = {EnemyType.DROID, EnemyType.BEAST, EnemyType.SITH, 
                            EnemyType.MERCENARY, EnemyType.CREATURE};
        EnemyType type = types[(int)(Math.random() * types.length)];
        int levelVariance = (int)(Math.random() * 3) - 1;
        int enemyLevel = Math.max(1, playerLevel + levelVariance);
        String name = generateName(type, enemyLevel);
        return new Enemy(name, type, enemyLevel);
    }
    
    private static String generateName(EnemyType type, int level) {
        String[] prefixes = {"Weak", "Young", "Feral", "Rogue", "Elite", "Corrupted"};
        String prefix = level > 5 ? prefixes[(int)(Math.random() * prefixes.length)] : "";
        
        switch (type) {
            case DROID: return (prefix.isEmpty() ? "" : prefix + " ") + "Battle Droid";
            case BEAST: return (prefix.isEmpty() ? "" : prefix + " ") + "Womp Rat";
            case SITH: return (prefix.isEmpty() ? "" : prefix + " ") + "Sith Acolyte";
            case MERCENARY: return (prefix.isEmpty() ? "" : prefix + " ") + "Mercenary";
            case CREATURE: return (prefix.isEmpty() ? "" : prefix + " ") + "Swamp Stalker";
            default: return "Unknown Enemy";
        }
    }
    
    public int calculatePhysicalDamage() {
        double variance = 0.9 + (Math.random() * 0.2);
        return Math.max(1, (int)(attack * variance));
    }
    
    public void takeDamage(int damage) {
        int actualDamage = Math.max(1, damage - (defense / 2));
        this.currentHealth = Math.max(0, currentHealth - actualDamage);
    }
    
    public boolean isAlive() { return currentHealth > 0; }
    
    public String getName() { return name; }
    public EnemyType getType() { return type; }
    public int getLevel() { return level; }
    public int getMaxHealth() { return maxHealth; }
    public int getCurrentHealth() { return currentHealth; }
    public double getHealthPercent() { return (double) currentHealth / maxHealth; }
    public int getXPReward() { return xpReward; }
    public int getGoldReward() { return goldReward; }
    public List<Item> getLoot() {
        List<Item> drops = new ArrayList<>();
        for (Item item : lootTable) {
            if (Math.random() < lootChance) drops.add(item);
        }
        return drops;
    }
}
