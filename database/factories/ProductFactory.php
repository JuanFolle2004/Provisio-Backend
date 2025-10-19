<?php

declare(strict_types=1);

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;
use Src\Groups\Domain\Model\Group;
use Src\Products\Domain\Model\Product;
use Src\Users\Domain\Models\User;

/**
 * @extends Factory<Product>
 */
class ProductFactory extends Factory
{
    protected $model = Product::class;

    public function definition(): array
    {
        return [
            'name' => fake()->word(),
            'group_id' => GroupFactory::new(),
            'amount' => fake()->numberBetween(1, 100),
        ];
    }
}