<?php

declare(strict_types=1);

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;
use Src\Assignment\Domain\Model\Assignment;
use Src\Groups\Domain\Model\Group;
use Src\Groups\Domain\Model\Thread;
use Src\Products\Domain\Model\Product;
use Src\Users\Domain\Models\User;

/**
 * @extends Factory<Thread>
 */
class ThreadFactory extends Factory
{
    protected $model = Thread::class;

    public function definition(): array
    {

        return [
            'group_id' => GroupFactory::new(),
        ];
    }
}