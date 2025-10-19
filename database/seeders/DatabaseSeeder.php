<?php

declare(strict_types=1);

namespace Database\Seeders;



use Database\Factories\AssignmentFactory;
use Database\Factories\GroupFactory;
use Database\Factories\ProductFactory;
use Database\Factories\UserFactory;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // Crear usuarios
        $users = UserFactory::new()->createMany(10);

        // Crear grupos
        $groups =GroupFactory::new()->createMany(5);

        // Asociar usuarios a grupos
        $users->each(function ($user) use ($groups) {
            $user->groups()->attach(
                $groups->random(rand(1, 3))->pluck('id'));
        });

        // Crear productos para cada grupo
        $groups->each(function ($group) {
            ProductFactory::new()->count(rand(5, 15))->create([
                'group_id' => $group->id,
            ]);
        });

        // Crear assignments (asignaciones)
        $groups->each(function ($group) {
            $products = $group->products;
            $groupUsers = $group->users;

            if ($groupUsers->isEmpty() || $products->isEmpty()) {
                return;
            }

            // Crear entre 10 y 20 asignaciones por grupo
            foreach (range(1, rand(10, 20)) as $i) {
                $product = $products->random();
                $maxAmount = $product->amount;

                AssignmentFactory::new()->create([
                    'user_id' => $groupUsers->random()->id,
                    'group_id' => $group->id,
                    'product_id' => $product->id,
                    'amount' => $amount = rand(1, min($maxAmount, 20)),
                    'bought' => rand(0, $amount),
                ]);
            }
        });
    }
}
