# Mario Kart 8 Deluxe Optimal Combos

This project uses the $docplex$ library in Python to find the optimal combination of driver, body, tires, and glider in
Mario Kart 8 Deluxe based on their associated statistics. The goal is to maximize the sum of the chosen parts' stats.

## Data

The script reads data from four CSV files (`drivers.csv`, `bodies.csv`, `tires.csv`, `gliders.csv`) located in a $data$
subdirectory. Each CSV file should have the first column as the unique identifier (e.g., driver name, body name) and
subsequent columns containing numerical statistics for that item.
This data has been extracted from
the [Mario Kart 8 Deluxe Wiki](https://www.mariowiki.com/Mario_Kart_8_Deluxe_in-game_statistics) and is available in the
$data$ folder.

The script then formulates an integer programming model to select at most one item from each category (driver, body,
tires, glider) such that the sum of their combined statistics is maximized.

## Prerequisites

* **Python 3.x:** (any version >= 3.6 and <= 3.8.x)
* **CPLEX Optimization Studio or CPLEX Python API ($docplex$):**
   $$`bash
   pip install cplex docplex
   $$`

## Stats

### Best overall combo

> [!NOTE]
> Just like Mario Kart 7 and Mario Kart 8, the game stores statistics for drivers and parts in points. In each
> statistics, the sum of the points for the driver, body, tires, and glider is a number potentially ranging from 0 to
> 20,
> called Level (Lv) in Mario Kart 7, that then determines the values of the related in-game statistics.
> Source: [Mario Kart 8 Deluxe Wiki](https://www.mariowiki.com/Mario_Kart_8_Deluxe_in-game_statistics)

Hence, to find the best overall combo, we need to find the combination of driver, body, tires, and glider that maximizes
the sum of their statistics. The script does this by creating a binary variable for each item in each category and
adding constraints to ensure that only one item from each category is selected.

#### Integer Linear Programming model
A very simple integer linear programming model is used to find optimal combinations.

The following sets are given as inputs:

- $D$: set of drivers
- $B$: set of bodies
- $T$: set of tires
- $G$: set of gliders

The following decision variables are defined:

- $d_i$: binary variable indicating whether driver $i$ is selected (1) or not (0)
- $b_i$: binary variable indicating whether body $i$ is selected (1) or not (0)
- $t_i$: binary variable indicating whether tire $i$ is selected (1) or not (0)
- $g_i$: binary variable indicating whether glider $i$ is selected (1) or not (0)

> These variables are needed to ensure that only one item from each category is selected.

For the sake of simplicity and brevity, the following notation is used:

- $ds_i$: the sum of all statistics for the driver $i$ (e.g., speed, acceleration, weight, handling, traction, etc.)
- $bs_i$: the sum of all statistics for the body $i$
- $ts_i$: the sum of all statistics for the tires $i$
- $gs_i$: the sum of all statistics for the glider $i$

For instance,

$$
ds\_(\text{biddybuggy}) = \text{Speed (Ground)} + \text{Speed (Water)} + \text{Speed (Air)} + \text{Speed (Anti-Gravity)} + \text{Acceleration (AC)} + \text{Weight (WG)} + \text{Handling (Ground)} + \text{Handling (Water)} + \text{Handling (Air)} + \text{Handling (Anti-Gravity)} + \text{(Off-Road) Traction (OF)} + \text{Mini-Turbo (MT)} + \text{Invincibility (IV)} + \text{On-Road Traction (ON)}
$$

$$
= 0 + 1 + 1 + 2 + 7 + 0 + 5 + 4 = 20
$$

Objective function (for the overall best combo):

$$
max \sum_{i=1}^{|D|} d_i \cdot ds_i + \sum_{i=1}^{|B|} b_i \cdot bs_i + \sum_{i=1}^{|T|} t_i \cdot ts_i + \sum_{i=1}^{|G|} g_i \cdot gs_i
$$

$s.t.$

$$
\sum_{i=1}^{|D|} d_i \leq 1 \quad\forall i \in D \quad\quad\text{(1)}
$$
$$
\sum_{i=1}^{|B|} b_i \leq 1 \quad\forall i \in B \quad\quad\text{(2)}
$$
$$
\sum_{i=1}^{|T|} t_i \leq 1 \quad\forall i \in T \quad\quad\text{(3)}
$$
$$
\sum_{i=1}^{|G|} g_i \leq 1 \quad\forall i \in G \quad\quad\text{(4)}
$$
$$
d_i, b_i, t_i, g_i \in \{0, 1\} \quad\forall i \in D, B, T, G
$$

Constraints $(1)$, $(2)$, $(3)$, and $(4)$ ensure that only one item from each category is selected.

> [!TIP]
> The intuition behind the objective function is that a given statistics are considered iff the corresponding
> item is selected (i.e. if the corresponding binary variable is 1), otherwise the sum of statistics is simply
> multiplied
> by 0.

This model has been used for all the combos in the table below. The only difference are the considered drivers (e.g. in
case of light/medium/heavy weight combos) or the stats considered. For instance, to obtain the fastest combo $ds_i$ is
computed as follows:

$$
ds_i = \text{Speed (Ground)} + \text{Speed (Water)} + \text{Speed (Air)} + \text{Speed (Anti-Gravity)}
$$

> [!WARNING]
> The model will select the first item in the list of drivers, bodies, tires, and gliders that has the maximum sum of
> statistics. Hence, these results are not necessarily the *unique* best combos.

#### Results

| Combo Type            | Driver                                                                                                                                                                        | Body                                                                                                                                                                                             | Tire                                                                                                                                                                                   | Glider                                                                                                                                                                                |
|-----------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Best Overall          | Petey Piranha    <img src="https://mario.wiki.gallery/images/8/86/MK8DX_Petey_Piranha_Icon.png" alt="Petey Piranha" style="height: 30px;  border-radius: 5px; padding: 2px;"> | Tanooki Kart <img src="https://mario.wiki.gallery/images/7/76/MK8_Tanooki_Buggy_Sprite.png" alt="Tanooki Kart" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;"> | GLA Tires     <img src="https://mario.wiki.gallery/images/b/ba/GLATires-MK8.png" alt="GLA Tires" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">     | Gold Glider  <img src="https://mario.wiki.gallery/images/1/18/GoldGliderMK8.png" alt="Gold Glider" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">  |
| Best Light Weight     | Baby Peach       <img src="https://mario.wiki.gallery/images/3/3d/MK8_BabyPeach_Icon.png" alt="Baby Peach" style="height: 30px;  border-radius: 5px; padding: 2px;">          | Tanooki Kart <img src="https://mario.wiki.gallery/images/7/76/MK8_Tanooki_Buggy_Sprite.png" alt="Tanooki Kart" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;"> | GLA Tires     <img src="https://mario.wiki.gallery/images/b/ba/GLATires-MK8.png" alt="GLA Tires" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">     | Gold Glider  <img src="https://mario.wiki.gallery/images/1/18/GoldGliderMK8.png" alt="Gold Glider" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">  |
| Best Medium Weight    | Iggy             <img src="https://mario.wiki.gallery/images/d/dd/MK8_Iggy_Icon.png" alt="Iggy" style="height: 30px;  border-radius: 5px; padding: 2px;">                     | Tanooki Kart <img src="https://mario.wiki.gallery/images/7/76/MK8_Tanooki_Buggy_Sprite.png" alt="Tanooki Kart" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;"> | GLA Tires     <img src="https://mario.wiki.gallery/images/b/ba/GLATires-MK8.png" alt="GLA Tires" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">     | Gold Glider  <img src="https://mario.wiki.gallery/images/1/18/GoldGliderMK8.png" alt="Gold Glider" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">  |
| Best Heavy Weight     | Petey Piranha    <img src="https://mario.wiki.gallery/images/8/86/MK8DX_Petey_Piranha_Icon.png" alt="Petey Piranha" style="height: 30px;  border-radius: 5px; padding: 2px;"> | Tanooki Kart <img src="https://mario.wiki.gallery/images/7/76/MK8_Tanooki_Buggy_Sprite.png" alt="Tanooki Kart" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;"> | GLA Tires     <img src="https://mario.wiki.gallery/images/b/ba/GLATires-MK8.png" alt="GLA Tires" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">     | Gold Glider  <img src="https://mario.wiki.gallery/images/1/18/GoldGliderMK8.png" alt="Gold Glider" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">  |
| Fastest Combo         | Morton           <img src="https://mario.wiki.gallery/images/7/72/MK8_Morton_Icon.png" alt="Morton" style="height: 30px;  border-radius: 5px; padding: 2px;">                 | Sports Coupe <img src="https://mario.wiki.gallery/images/f/f8/SportsCoupeMK8.png" alt="Sports Coupe" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">           | Wood (Wooden) <img src="https://mario.wiki.gallery/images/0/03/WoodTiresMK8.png" alt="Wood (Wooden)" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;"> | Hylian Kite  <img src="https://mario.wiki.gallery/images/9/9c/MK8-HylianKite.png" alt="Hylian Kite" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;"> |
| Highest Acceleration  | Toadette         <img src="https://mario.wiki.gallery/images/8/8e/MK8_Toadette_Icon.png" alt="Toadette" style="height: 30px;  border-radius: 5px; padding: 2px;">             | Biddybuggy   <img src="https://mario.wiki.gallery/images/4/45/BiddybuggyBodyMK8.png" alt="Biddybuggy" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">          | Roller        <img src="https://mario.wiki.gallery/images/7/76/RollerTiresMK8.png" alt="Roller" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">      | Cloud Glider <img src="https://mario.wiki.gallery/images/8/84/Cloud_Glider.png" alt="Cloud Glider" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">  |
| Highest Handling      | Baby Peach       <img src="https://mario.wiki.gallery/images/3/3d/MK8_BabyPeach_Icon.png" alt="Baby Peach" style="height: 30px;  border-radius: 5px; padding: 2px;">          | Biddybuggy   <img src="https://mario.wiki.gallery/images/4/45/BiddybuggyBodyMK8.png" alt="Biddybuggy" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">          | Roller        <img src="https://mario.wiki.gallery/images/7/76/RollerTiresMK8.png" alt="Roller" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">      | Cloud Glider <img src="https://mario.wiki.gallery/images/8/84/Cloud_Glider.png" alt="Cloud Glider" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">  |
| Highest Invincibility | Baby Peach       <img src="https://mario.wiki.gallery/images/3/3d/MK8_BabyPeach_Icon.png" alt="Baby Peach" style="height: 30px;  border-radius: 5px; padding: 2px;">          | Flame Rider  <img src="https://mario.wiki.gallery/images/3/31/FlameRiderBodyMK8.png" alt="Flame Rider" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">         | Monster       <img src="https://mario.wiki.gallery/images/2/29/MonsterTiresMK8.png" alt="Monster" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">    | Wario Wing   <img src="https://mario.wiki.gallery/images/a/ae/WarioWingMK8.png" alt="Wario Wing" style="height: 30px; border: 1px solid black; border-radius: 5px; padding: 2px;">    |

