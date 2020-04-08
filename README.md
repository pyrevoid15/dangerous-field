# dangerous-field
A bullet-hell-esque game of my creation.

Survive through all 17 levels of various quantities of enemies and claim victory.  I may add more later, but this is what there is right now.  By default, the game may be set to the debug level.  To actually progress through the game, change the starting level tag in the Game class to 0.  As I continue to add things to this game, this will change.

### About the player
-Use arrow keys to move in any direction.

-Use SHIFT key to dash, giving the player invulnerability and a speed boost at the cost of energy.

-Dashing can only be done if the player has energy, which replenishes over time.

-Use ESCAPE to pause the game.

### Here are the enemy types that exist right now:
-Chaser(normal):  This large black enemy will almost always travel directly towards the player.  Occasionally, it may charge at the player, during which it will not follow behind the player.

-Chaser(special): Similarly to the normal Chaser, this enemy will follow the player and eventually charge the player.  However, this enemy will also occassionally teleport to a different location.  As a result, this enemy often teams up with the normal Chaser and other special Chasers.

-Tumbleweed:  Bounces off from walls at light speed...

-Archer(normal): This normal archer will move around and shoot projectiles directly toward the player.  These projectiles can be blocked by bushes littered throughout the world.  Darker projectiles are faster than normal and will **NOT** be blocked by bushes.

-Archer(crazy): This enemy is similar to the archer, but will not shoot directly at the player.  It will shoot in every direction.

-Vortal:  This enemy occasionally captures projectiles from Archer-type enemies (denoted by red color) and will either disperse them immediately in a direction directly away from itself or will move them toward itself to be ejected diagonally or directly vertical or horizontal in direction.

-Trapper: This enemy will attempt to avoid the player, but will will lay mines in its travels.

-Laserist: This enemy will move from place to place, often releasing one or more blue lasers that deal damage on contact without invincibility frames.  The end of the laser does instant damage comparable to a trapper's mine.  When shooting its lasers, it may rotate, allowing it to sweep large areas of the field.  Standing close to the laserist when it is shooting deals damage.  A wider area around the laserist allows the player to gain energy faster.
