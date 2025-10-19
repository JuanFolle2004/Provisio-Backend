<?php

declare(strict_types=1);

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;
use Src\Assignment\Domain\Model\Assignment;
use Src\Groups\Domain\Model\Group;
use Src\Products\Domain\Model\Product;
use Src\Users\Domain\Models\User;

/**
 * @extends Factory<Assignment>
 */
class AssignmentFactory extends Factory
{
    protected $model = Assignment::class;

    public function definition(): array
    {
        $amount = fake()->numberBetween(1, 50);

        return [
            'user_id' => UserFactory::new(),
            'group_id' => GroupFactory::new(),
            'product_id' => ProductFactory::new(),
            'amount' => $amount,
            'bought' => fake()->numberBetween(0, $amount),
        ];
    }
}