<?php

declare(strict_types=1);

namespace Src\Groups\Domain\Dtos;

use Carbon\CarbonImmutable;

class GameDto
{
    public function __construct(
        public string $name,
        public CarbonImmutable $dueDate,
    ) {
    }
}
