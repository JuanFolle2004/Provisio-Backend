<?php

declare(strict_types=1);

namespace Src\Users\Domain\DataTransferObjects;

class UserDto
{
    public function __construct(
        public readonly string $name,
        public readonly string $emailAddress,
        public readonly string $password,
        public readonly string $username,
    ) {
    }
}
