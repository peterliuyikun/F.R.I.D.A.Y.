package com.friday.rpg.core;

import com.friday.rpg.inventory.Equipment;
import com.friday.rpg.inventory.Inventory;
import com.friday.rpg.map.Position;

import java.io.Serializable;

public class Player implements Serializable {
    private static final long serialVersionUID = 1L;
    
    private String name;
    private Position position;
    
    private int level;
    private int experience;
    private int experienceToNext;
    
    private int strength;
    private int dexterity;
    private int intelligence;
    private int vitality;
    private int wisdom;
    
    private int maxHealth;
    private int currentHealth;
    private int maxMana;
    private int currentMana;
    
    private int attack;
    private int defense;
    private int magicAttack;
    private int magicDefense;
    private int speed;
    private int critChance;
    
    private int gold;
    private Inventory inventory;
    private Equipment equipment;
    
    public Player(String name) {
        this.name = name;
        this.position = new Position(25, 25);
        
        this.level = 1;
        this.experience = 0;
        this.experienceToNext = 100;
        
        this.strength = 10;
        this.dexterity = 10;
        this.intelligence = 10;
        this.vitality = 10;
        this.wisdom = 10;
        
        this.gold = 100;
        this.inventory = new Inventory(40);
        this.equipment = new Equipment();
        
        recalculateStats();
        this.currentHealth = maxHealth;
        this.currentMana = maxMana;
    }
    
    public void recalculateStats() {
        this.maxHealth = 50 + (vitality * 10) + (level * 5);
        this.maxMana = 20 + (wisdom * 8) + (level * 3);
        
        this.attack = strength * 2 + equipment.getTotalAttack();
        this.defense = (strength + dexterity) + equipment.getTotalDefense();
        this.magicAttack = intelligence * 2 + equipment.getTotalMagicAttack();
        this.magicDefense = (intelligence + wisdom) + equipment.getTotalMagicDefense();
        this.speed = dexterity + equipment.getTotalSpeed();
        this.critChance = Math.min(5 + (dexterity / 5), 50);
        
        this.currentHealth = Math.min(currentHealth, maxHealth);
        this.currentMana = Math.min(currentMana, maxMana);
    }
    
    public void gainExperience(int amount) {
        this.experience += amount;
        while (this.experience >= this.experienceToNext) {
            levelUp();
        }
    }
    
    private void levelUp() {
        this.experience -= this.experienceToNext;
        this.level++;
        this.experienceToNext = (int)(100 * Math.pow(1.2, level - 1));
        recalculateStats();
        this.currentHealth = maxHealth;
        this.currentMana = maxMana;
    }
    
    public int calculatePhysicalDamage() {
        int baseDamage = attack;
        double variance = 0.9 + (Math.random() * 0.2);
        boolean isCrit = Math.random() * 100 < critChance;
        int damage = (int)(baseDamage * variance);
        if (isCrit) damage *= 2;
        return Math.max(1, damage);
    }
    
    public void takeDamage(int damage) {
        int actualDamage = Math.max(1, damage - (defense / 2));
        this.currentHealth = Math.max(0, currentHealth - actualDamage);
    }
    
    public void heal(int amount) {
        this.currentHealth = Math.min(maxHealth, currentHealth + amount);
    }
    
    public boolean isAlive() { return currentHealth > 0; }
    
    public String getName() { return name; }
    public Position getPosition() { return position; }
    public void setPosition(Position pos) { this.position = pos; }
    public int getLevel() { return level; }
    public int getExperience() { return experience; }
    public int getExperienceToNext() { return experienceToNext; }
    public double getExperiencePercent() { return (double) experience / experienceToNext; }
    public int getStrength() { return strength; }
    public int getDexterity() { return dexterity; }
    public int getIntelligence() { return intelligence; }
    public int getVitality() { return vitality; }
    public int getWisdom() { return wisdom; }
    public int getMaxHealth() { return maxHealth; }
    public int getCurrentHealth() { return currentHealth; }
    public double getHealthPercent() { return (double) currentHealth / maxHealth; }
    public int getMaxMana() { return maxMana; }
    public int getCurrentMana() { return currentMana; }
    public double getManaPercent() { return (double) currentMana / maxMana; }
    public int getAttack() { return attack; }
    public int getDefense() { return defense; }
    public int getMagicAttack() { return magicAttack; }
    public int getMagicDefense() { return magicDefense; }
    public int getSpeed() { return speed; }
    public int getCritChance() { return critChance; }
    public int getGold() { return gold; }
    public void addGold(int amount) { this.gold += amount; }
    public Inventory getInventory() { return inventory; }
    public Equipment getEquipment() { return equipment; }
}
