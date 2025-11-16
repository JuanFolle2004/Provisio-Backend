<?php

declare(strict_types=1);

namespace Src\Groups\Domain\Dtos;

use Src\Groups\Domain\Model\Group;
use Src\Users\Domain\Models\User;

readonly class MessageDto
{
    public function __construct(
        public User $user,
        public Group $group,
        public string $content,
    ) {
    }
}
