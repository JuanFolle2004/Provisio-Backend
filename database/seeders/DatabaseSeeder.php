<?php

declare(strict_types=1);

namespace Database\Seeders;



use Database\Factories\AssignmentFactory;
use Database\Factories\GroupFactory;
use Database\Factories\MessageFactory;
use Database\Factories\ProductFactory;
use Database\Factories\ThreadFactory;
use Database\Factories\UserFactory;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    public function run(): void
    {
        // Crear usuarios
        $users = UserFactory::new()->createMany(10);

        // Crear grupos
        $groups = GroupFactory::new()->createMany(5);

        // Asociar usuarios a grupos
        $users->each(function ($user) use ($groups) {
            $user->groups()->attach(
                $groups->random(rand(1, 3))->pluck('id')
            );
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

            // Rastrear cuánto se ha asignado de cada producto
            $productAssignments = [];

            // Crear entre 10 y 20 asignaciones por grupo
            foreach (range(1, rand(10, 20)) as $i) {
                $product = $products->random();
                $productId = $product->id;

                // Inicializar si no existe
                if (!isset($productAssignments[$productId])) {
                    $productAssignments[$productId] = 0;
                }

                // Calcular cuánto queda disponible
                $alreadyAssigned = $productAssignments[$productId];
                $remaining = $product->amount - $alreadyAssigned;

                // Si no queda nada disponible, elegir otro producto
                if ($remaining <= 0) {
                    continue;
                }

                // Asignar como máximo lo que queda disponible
                $amount = rand(1, min($remaining, 20));

                AssignmentFactory::new()->create([
                    'user_id' => $groupUsers->random()->id,
                    'group_id' => $group->id,
                    'product_id' => $productId,
                    'amount' => $amount,
                    'bought' => rand(0, $amount),
                ]);

                // Actualizar el registro de asignaciones
                $productAssignments[$productId] += $amount;
            }
        });

        // Crear threads para cada grupo
        $groups->each(function ($group) {
            $thread = ThreadFactory::new()->createOne([
                'group_id' => $group->id,
            ]);

            // Obtener usuarios del grupo
            $groupUsers = $group->users;

            if ($groupUsers->isEmpty()) {
                return;
            }

            // Crear entre 5 y 20 mensajes por thread
            foreach (range(1, rand(5, 20)) as $i) {
                MessageFactory::new()->create([
                    'user_id' => $groupUsers->random()->id,
                    'thread_id' => $thread->id,
                    'content' => fake()->paragraphs(rand(1, 3), true),
                ]);
            }
        });
    }
}
