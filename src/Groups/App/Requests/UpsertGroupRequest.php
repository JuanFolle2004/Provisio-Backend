<?php

declare(strict_types=1);

namespace Src\Groups\App\Requests;

use Illuminate\Foundation\Http\FormRequest;
use Src\Groups\Domain\Dtos\GameDto;

class UpsertGroupRequest extends FormRequest
{
    public function rules(): array
    {
        return [
            'name'=>['required', 'string'],
            'due_date'=>['required', 'date', 'date_format:Y-m-d', 'after_or_equal:today'],
        ];
    }

    public function toDto(): \Src\Groups\Domain\Dtos\GameDto
    {
        /** @var \Carbon\CarbonImmutable $due_date */
        $due_date = $this->date('due_date');

        return new GameDto(
            name: $this->string('name')->toString(),
            dueDate: $due_date->toImmutable(),
        );
    }
}
