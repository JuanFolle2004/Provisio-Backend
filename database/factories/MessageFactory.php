<?php

declare(strict_types=1);

namespace Database\Factories;

use Illuminate\Database\Eloquent\Factories\Factory;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Str;
use Src\Assignment\Domain\Model\Assignment;
use Src\Groups\Domain\Model\Group;
use Src\Groups\Domain\Model\Message;
use Src\Groups\Domain\Model\Thread;
use Src\Products\Domain\Model\Product;
use Src\Users\Domain\Models\User;

/**
 * @extends Factory<Thread>
 */
class MessageFactory extends Factory
{
    /** @phpstan-ignore-next-line */
    protected $model = Message::class;

    public function definition(): array
    {
        return [
            'user_id' => UserFactory::new(),
            'thread_id' => ThreadFactory::new(),
            'content' => fake()->paragraphs(rand(1, 3), true),
        ];
    }
}